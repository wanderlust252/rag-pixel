import { FormEvent, useEffect, useMemo, useRef, useState } from "react";

import {
  changeCharacter,
  createSession,
  getCharacters,
  getWorld,
  interact,
  queryRag,
  syncPosition,
} from "./api";
import { findNearestTarget, movePosition } from "./gameLogic";
import type {
  Direction,
  GameCharacter,
  GameSession,
  GameWorld,
  InteractionResponse,
  InteractableTarget,
  Position,
  QueryFilters,
  QueryResponse,
} from "./types";

const DEFAULT_DIRECTION: Direction = "down";
const MOVEMENT_INTERVAL_MS = 48;
const PORTAL_IMAGE = "/assets/portals/simple/portal-00.png";

function App() {
  const [characters, setCharacters] = useState<GameCharacter[]>([]);
  const [world, setWorld] = useState<GameWorld | null>(null);
  const [session, setSession] = useState<GameSession | null>(null);
  const [position, setPosition] = useState<Position>({ x: 96, y: 520 });
  const [direction, setDirection] = useState<Direction>(DEFAULT_DIRECTION);
  const [activeDirection, setActiveDirection] = useState<Direction | null>(null);
  const [moving, setMoving] = useState(false);
  const [frame, setFrame] = useState(0);
  const [interaction, setInteraction] = useState<InteractionResponse | null>(null);
  const [activeTarget, setActiveTarget] = useState<InteractableTarget | null>(null);
  const [chatOpen, setChatOpen] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const pressedDirectionsRef = useRef<Direction[]>([]);

  useEffect(() => {
    let cancelled = false;
    Promise.all([getCharacters(), getWorld()])
      .then(([loadedCharacters, loadedWorld]) => {
        if (cancelled) return;
        setCharacters(loadedCharacters);
        setWorld(loadedWorld);
        setPosition(loadedWorld.spawn);
      })
      .catch(() => setError("Không tải được dữ liệu phase 2. Kiểm tra backend ở port 8000."))
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, []);

  useEffect(() => {
    if (!moving || !session) return undefined;
    const animation = session.character.sprite.animations.find((item) => item.name === direction);
    const interval = window.setInterval(() => {
      setFrame((current) => (current + 1) % (animation?.frames ?? 1));
    }, animation?.frame_duration_ms ?? 120);
    return () => window.clearInterval(interval);
  }, [direction, moving, session]);

  useEffect(() => {
    if (!session) return undefined;
    const timeout = window.setTimeout(() => {
      syncPosition(session.session_id, position).catch(() => undefined);
    }, 250);
    return () => window.clearTimeout(timeout);
  }, [position, session]);

  useEffect(() => {
    if (!world || !session || !activeDirection) return undefined;

    setMoving(true);
    const interval = window.setInterval(() => {
      setPosition((current) => movePosition(current, activeDirection, world));
    }, MOVEMENT_INTERVAL_MS);

    return () => window.clearInterval(interval);
  }, [activeDirection, session, world]);

  useEffect(() => {
    if (activeDirection) return;
    setMoving(false);
    pressedDirectionsRef.current = [];
  }, [activeDirection]);

  const nearestTarget = useMemo(() => {
    if (!world || !session) return null;
    return findNearestTarget(position, world);
  }, [position, session, world]);

  const chatScope = useMemo(() => {
    if (!world) return null;
    return buildChatScope({ interaction, activeTarget, world });
  }, [activeTarget, interaction, world]);

  useEffect(() => {
    if (!chatScope) {
      setChatOpen(false);
    }
  }, [chatScope]);

  useEffect(() => {
    if (!chatOpen) return undefined;
    const { overflow } = document.body.style;
    document.body.style.overflow = "hidden";
    return () => {
      document.body.style.overflow = overflow;
    };
  }, [chatOpen]);

  useEffect(() => {
    if (!world || !session) return undefined;

    const onKeyDown = (event: KeyboardEvent) => {
      if (event.target instanceof HTMLInputElement) return;
      const nextDirection = directionFromKey(event.key);
      if (nextDirection) {
        event.preventDefault();
        const alreadyPressed = pressedDirectionsRef.current.includes(nextDirection);
        pressedDirectionsRef.current = [
          ...pressedDirectionsRef.current.filter((item) => item !== nextDirection),
          nextDirection,
        ];
        setDirection(nextDirection);
        setActiveDirection(nextDirection);
        setInteraction(null);
        setActiveTarget(null);
        if (!alreadyPressed) {
          setPosition((current) => movePosition(current, nextDirection, world));
        }
      }
      if (event.key.toLowerCase() === "e") {
        event.preventDefault();
        void runInteraction(nearestTarget);
      }
    };

    const onKeyUp = (event: KeyboardEvent) => {
      const releasedDirection = directionFromKey(event.key);
      if (!releasedDirection) return;

      pressedDirectionsRef.current = pressedDirectionsRef.current.filter(
        (item) => item !== releasedDirection,
      );
      const nextDirection = pressedDirectionsRef.current.at(-1) ?? null;
      setActiveDirection(nextDirection);
      if (nextDirection) {
        setDirection(nextDirection);
      }
    };

    window.addEventListener("keydown", onKeyDown);
    window.addEventListener("keyup", onKeyUp);
    return () => {
      window.removeEventListener("keydown", onKeyDown);
      window.removeEventListener("keyup", onKeyUp);
    };
  }, [nearestTarget, session, world]);

  async function handleCreateSession(input: {
    userName: string;
    displayName: string;
    characterId: string;
  }) {
    setError(null);
    const nextSession = await createSession(input);
    setSession(nextSession);
    setPosition(nextSession.position);
  }

  async function handleChangeCharacter(characterId: string) {
    if (!session) return;
    setError(null);
    const updated = await changeCharacter(session.session_id, characterId);
    setSession(updated);
  }

  async function runInteraction(target: InteractableTarget | null) {
    if (!session || !target) return;
    setError(null);
    setActiveTarget(target);
    const result = await interact({
      sessionId: session.session_id,
      targetType: target.type,
      targetId: target.id,
    });
    setInteraction(result);
  }

  if (loading) {
    return <main className="loading">Loading RAG Pixels</main>;
  }

  if (!world) {
    return <main className="loading">{error ?? "World unavailable"}</main>;
  }

  return (
    <main className="app-shell">
      <section className="top-bar">
        <div>
          <p className="eyebrow">Phase 2</p>
          <h1>RAG Pixels Library</h1>
        </div>
        {session && (
          <div className="player-chip">
            <span>{session.display_name}</span>
            <strong>{session.character.display_name}</strong>
          </div>
        )}
      </section>

      {error && <div className="error-banner">{error}</div>}

      {!session ? (
        <SessionGate
          characters={characters}
          onSubmit={(input) => {
            handleCreateSession(input).catch(() =>
              setError("Không tạo được session. userName chỉ dùng chữ, số, _ hoặc -."),
            );
          }}
        />
      ) : (
        <section className="game-layout">
          <aside className="side-panel">
            <CharacterSwitcher
              characters={characters}
              activeCharacterId={session.character.character_id}
              onChange={(characterId) => {
                handleChangeCharacter(characterId).catch(() =>
                  setError("Không đổi được nhân vật."),
                );
              }}
            />
            <InteractionPanel
              nearestTarget={nearestTarget}
              activeTarget={activeTarget}
              interaction={interaction}
              world={world}
              onInteract={() => {
                runInteraction(nearestTarget).catch(() => setError("Không tương tác được mục này."));
              }}
            />
          </aside>

          <GameStage
            world={world}
            session={session}
            position={position}
            direction={direction}
            frame={moving ? frame : 0}
            nearestTarget={nearestTarget}
            onTargetClick={(target) => {
              runInteraction(target).catch(() => setError("Không tương tác được mục này."));
            }}
          />
        </section>
      )}

      {chatScope && session && (
        <>
          <button
            aria-controls="rag-chat-modal"
            aria-expanded={chatOpen}
            aria-haspopup="dialog"
            className="chat-launcher"
            type="button"
            onClick={() => setChatOpen(true)}
          >
            <span>RAG Chat</span>
            <strong>{chatScope.label}</strong>
          </button>
          {chatOpen && (
            <ChatModal scope={chatScope} onAsk={(question, filters) => queryRag({ question, filters })} onClose={() => setChatOpen(false)} />
          )}
        </>
      )}
    </main>
  );
}

function SessionGate({
  characters,
  onSubmit,
}: {
  characters: GameCharacter[];
  onSubmit: (input: { userName: string; displayName: string; characterId: string }) => void;
}) {
  const [userName, setUserName] = useState("tester_01");
  const [displayName, setDisplayName] = useState("Pixel Tester");
  const [characterId, setCharacterId] = useState(characters[0]?.character_id ?? "");

  useEffect(() => {
    if (!characterId && characters[0]) {
      setCharacterId(characters[0].character_id);
    }
  }, [characterId, characters]);

  function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    onSubmit({ userName, displayName, characterId });
  }

  return (
    <form className="session-gate" onSubmit={submit}>
      <label>
        userName
        <input value={userName} onChange={(event) => setUserName(event.target.value)} />
      </label>
      <label>
        displayName
        <input value={displayName} onChange={(event) => setDisplayName(event.target.value)} />
      </label>
      <div className="character-grid">
        {characters.map((character) => (
          <button
            className={character.character_id === characterId ? "character-card active" : "character-card"}
            key={character.character_id}
            type="button"
            onClick={() => setCharacterId(character.character_id)}
          >
            <Sprite character={character} direction="down" frame={0} />
            <span>{character.display_name}</span>
          </button>
        ))}
      </div>
      <button className="primary-action" type="submit">
        Enter Library
      </button>
    </form>
  );
}

function CharacterSwitcher({
  characters,
  activeCharacterId,
  onChange,
}: {
  characters: GameCharacter[];
  activeCharacterId: string;
  onChange: (characterId: string) => void;
}) {
  return (
    <section>
      <h2>Nhân vật</h2>
      <div className="switcher-list">
        {characters.map((character) => (
          <button
            className={character.character_id === activeCharacterId ? "switcher active" : "switcher"}
            key={character.character_id}
            type="button"
            onClick={() => onChange(character.character_id)}
          >
            <Sprite character={character} direction="down" frame={0} compact />
            <span>{character.display_name}</span>
          </button>
        ))}
      </div>
    </section>
  );
}

function InteractionPanel({
  nearestTarget,
  activeTarget,
  interaction,
  world,
  onInteract,
}: {
  nearestTarget: InteractableTarget | null;
  activeTarget: InteractableTarget | null;
  interaction: InteractionResponse | null;
  world: GameWorld;
  onInteract: () => void;
}) {
  const chatScope = useMemo(() => buildChatScope({ interaction, activeTarget, world }), [
    activeTarget,
    interaction,
    world,
  ]);

  return (
    <section>
      <h2>Tương tác</h2>
      <button className="primary-action" disabled={!nearestTarget} type="button" onClick={onInteract}>
        {nearestTarget ? nearestTarget.label : "Chưa có mục gần"}
      </button>
      {interaction && (
        <div className="interaction-result">
          <h3>{interaction.title}</h3>
          <p>{interaction.message}</p>
          {interaction.document && (
            <dl>
              <dt>doc_id</dt>
              <dd>{interaction.document.doc_id}</dd>
              <dt>doc_type</dt>
              <dd>{interaction.document.doc_type}</dd>
              <dt>source</dt>
              <dd>{interaction.document.source_path}</dd>
            </dl>
          )}
          {interaction.related_documents.length > 0 && (
            <ul>
              {interaction.related_documents.map((document) => (
                <li key={document.doc_id}>{document.title}</li>
              ))}
            </ul>
          )}
        </div>
      )}
      {chatScope && (
        <div className="chat-hint">
          <div className="scope-chip">
            <span>Chat scope</span>
            <strong>{chatScope.label}</strong>
          </div>
          <p>Mở cửa sổ chat ở góc dưới phải để hỏi trong phạm vi này.</p>
        </div>
      )}
    </section>
  );
}

type ChatScope = {
  key: string;
  label: string;
  filters: QueryFilters;
};

function ChatModal({
  scope,
  onAsk,
  onClose,
}: {
  scope: ChatScope;
  onAsk: (question: string, filters: QueryFilters) => Promise<QueryResponse>;
  onClose: () => void;
}) {
  const [question, setQuestion] = useState("");
  const [history, setHistory] = useState<
    { question: string; response: QueryResponse | null; error?: string }[]
  >([]);
  const [asking, setAsking] = useState(false);
  const [pendingQuestion, setPendingQuestion] = useState<string | null>(null);
  const inputRef = useRef<HTMLInputElement | null>(null);

  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  useEffect(() => {
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") {
        event.preventDefault();
        onClose();
      }
    };

    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, [onClose]);

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const trimmed = question.trim();
    if (!trimmed || asking) return;

    setQuestion("");
    setAsking(true);
    setPendingQuestion(trimmed);
    try {
      const response = await onAsk(trimmed, scope.filters);
      setHistory((current) => [...current, { question: trimmed, response }]);
    } catch (error) {
      setHistory((current) => [
        ...current,
        {
          question: trimmed,
          response: null,
          error: error instanceof Error ? error.message : "Không truy vấn được RAG.",
        },
      ]);
    } finally {
      setAsking(false);
      setPendingQuestion(null);
    }
  }

  return (
    <div className="chat-modal-overlay" role="presentation" onClick={onClose}>
      <section
        aria-labelledby="rag-chat-title"
        aria-modal="true"
        className="chat-modal"
        id="rag-chat-modal"
        role="dialog"
        onClick={(event) => event.stopPropagation()}
      >
        <div className="chat-modal-header">
          <div>
            <p className="eyebrow">RAG chat</p>
            <h2 id="rag-chat-title">Hỏi trong phạm vi hiện tại</h2>
          </div>
          <button aria-label="Đóng chat" className="chat-close" type="button" onClick={onClose}>
            x
          </button>
        </div>
        <div className="scoped-chat" key={scope.key}>
          <div className="scope-chip">
            <span>Scope</span>
            <strong>{scope.label}</strong>
          </div>
          <form onSubmit={submit}>
            <input
              ref={inputRef}
              value={question}
              onChange={(event) => setQuestion(event.target.value)}
              placeholder="Hỏi trong phạm vi này"
            />
            <button className="primary-action" disabled={asking || !question.trim()} type="submit">
              {asking ? "..." : "Hỏi"}
            </button>
          </form>
          {asking && pendingQuestion && (
            <div className="chat-status" role="status" aria-live="polite">
              Đang truy vấn: {pendingQuestion}
            </div>
          )}
          <div className="chat-history">
            {asking && pendingQuestion && (
              <article className="chat-history pending">
                <h3>{pendingQuestion}</h3>
                <p>Đang chờ RAG phản hồi...</p>
              </article>
            )}
            {history.map((item, index) => (
              <article key={`${item.question}-${index}`}>
                <h3>{item.question}</h3>
                {item.error ? (
                  <p>{item.error}</p>
                ) : (
                  <>
                    <p>{item.response?.answer}</p>
                    {item.response && item.response.sources.length > 0 && (
                      <ul>
                        {item.response.sources.slice(0, 3).map((source, sourceIndex) => (
                          <li key={`${source.doc_id}-${sourceIndex}`}>
                            <strong>{source.title ?? source.doc_id}</strong>
                            <span>{source.snippet}</span>
                          </li>
                        ))}
                      </ul>
                    )}
                  </>
                )}
              </article>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}

function buildChatScopeKey(filters: QueryFilters) {
  return JSON.stringify(filters, Object.keys(filters).sort());
}

function buildChatScope({
  interaction,
  activeTarget,
  world,
}: {
  interaction: InteractionResponse | null;
  activeTarget: InteractableTarget | null;
  world: GameWorld;
}): ChatScope | null {
  if (interaction?.document) {
    const filters = { doc_id: interaction.document.doc_id };
    return {
      key: buildChatScopeKey(filters),
      label: interaction.document.title,
      filters,
    };
  }

  if (activeTarget?.type === "portal") {
    const portal = world.portals.find((item) => item.portal_id === activeTarget.id);
    if (!portal) return null;
    const portalDocuments = world.shelves
      .filter((shelf) => shelf.portal_id === portal.portal_id)
      .map((shelf) => shelf.document);
    const filters = portalDocuments.some((document) => document.room_id === portal.portal_id)
      ? { room_id: portal.portal_id }
      : { business_flow: portal.business_flow };
    return {
      key: buildChatScopeKey(filters),
      label: portal.label,
      filters,
    };
  }

  return null;
}

function GameStage({
  world,
  session,
  position,
  direction,
  frame,
  nearestTarget,
  onTargetClick,
}: {
  world: GameWorld;
  session: GameSession;
  position: Position;
  direction: Direction;
  frame: number;
  nearestTarget: InteractableTarget | null;
  onTargetClick: (target: InteractableTarget) => void;
}) {
  return (
    <section className="stage-wrap" aria-label={world.name}>
      <div className="stage" style={{ width: world.width, height: world.height }}>
        <div className="back-wall" />
        {world.portals.map((portal) => {
          const active = nearestTarget?.type === "portal" && nearestTarget.id === portal.portal_id;
          return (
            <button
              className={active ? "portal active" : "portal"}
              key={portal.portal_id}
              type="button"
              style={{
                left: portal.position.x,
                top: portal.position.y,
                backgroundImage: `url(${PORTAL_IMAGE})`,
              }}
              onClick={() =>
                onTargetClick({
                  type: "portal",
                  id: portal.portal_id,
                  label: portal.label,
                  position: portal.position,
                })
              }
              title={portal.label}
            >
              <span className="portal-caption">
                <span>{portal.label}</span>
                <small>{portal.document_count}</small>
              </span>
            </button>
          );
        })}

        {world.shelves.map((shelf) => {
          const active = nearestTarget?.type === "bookshelf" && nearestTarget.id === shelf.shelf_id;
          return (
            <button
              className={active ? "shelf active" : "shelf"}
              key={shelf.shelf_id}
              type="button"
              style={{ left: shelf.position.x, top: shelf.position.y }}
              onClick={() =>
                onTargetClick({
                  type: "bookshelf",
                  id: shelf.shelf_id,
                  label: shelf.label,
                  position: shelf.position,
                })
              }
              title={shelf.label}
            >
              <span>{shelf.doc_type}</span>
            </button>
          );
        })}

        <div className="avatar" style={{ left: position.x, top: position.y }}>
          <Sprite character={session.character} direction={direction} frame={frame} />
          <span>{session.display_name}</span>
        </div>
      </div>
    </section>
  );
}

function Sprite({
  character,
  direction,
  frame,
  compact = false,
}: {
  character: GameCharacter;
  direction: Direction;
  frame: number;
  compact?: boolean;
}) {
  const animation =
    character.sprite.animations.find((item) => item.name === direction) ?? character.sprite.animations[0];
  const frameIndex = frame % animation.frames;
  const width = character.sprite.frame_width;
  const height = character.sprite.frame_height;
  const scale = compact ? 0.625 : 1;

  return (
    <span
      className="sprite"
      style={{
        width,
        height,
        transform: `scale(${scale})`,
        margin: compact ? "-12px -10px" : undefined,
        backgroundImage: `url(${character.sprite.image_url})`,
        backgroundPosition: `-${frameIndex * width}px -${animation.row * height}px`,
      }}
    />
  );
}

function directionFromKey(key: string): Direction | null {
  const normalized = key.toLowerCase();
  if (normalized === "arrowup" || normalized === "w") return "up";
  if (normalized === "arrowdown" || normalized === "s") return "down";
  if (normalized === "arrowleft" || normalized === "a") return "left";
  if (normalized === "arrowright" || normalized === "d") return "right";
  return null;
}

export default App;
