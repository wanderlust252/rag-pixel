# SRS Luong khoan Metfone 20260515

TRIỂN KHAI PHẦN MỀM HỆ THỐNG  SCS

TỔNG CÔNG TY CỔ PHẦN BƯU CHÍNH VIETTEL

TÀI LIỆU ĐẶC TẢ HỆ THỐNG

LƯƠNG KHOÁN SCS METFONE

| # | # |
|---|---|
|Số hợp đồng||
|Mã dự án||
|Mã hiệu tài liệu:||
|Phiên bản tài liệu:|1.0.3|
|Ngày cập nhật:|25/04/2026|

Hà Nội, năm 2026<div class="page"></div>

TRANG KÝ

| # | # | # |
|---|---|---|
|Vai trò|Biên soạn|Yêu cầu|
|Chữ ký|||

<div class="page"></div>

LỊCH SỬ THAY ĐỔI

| # | # | # | # | # | # |
|---|---|---|---|---|---|
|Ngày|Phiên bản|Người thực hiện|Mục, bảng, sơ đồ được thay đổi|Loại|Mô tả|
|04/12/2025|1.0.0|Phạm Ánh Cẩm Nhung||Tạo mới||
|06/04/2026|1.0.1|Phạm Ánh Cẩm Nhung||Điều chỉnh|1. Bổ sung sự kiện hoàn thành chuyến xe;<br>2. Điều chỉnh các luồng đồng bộ master data:<br>- Nhân sự:<br>+ Nâng tần suất đồng bộ lên real-time;<br>+ Bổ sung chức danh & loại hợp đồng;<br>- Chi nhánh: Nâng tần suất đồng bộ lên real-time;<br>- Bưu cục: Nâng tần suất đồng bộ lên real-time;<br>3. Bổ sung luồng tính lương từ sự kiện hoàn thành chuyến xe.|
|18/04/2026|1.0.2|Phạm Ánh Cẩm Nhung||Điều chỉnh||
|25/04/2026|1.0.3|Phạm Ánh Cẩm Nhung||Điều chỉnh|1. Đồng bộ thêm một số master data từ OPS: Danh mục chức danh & Danh mục đối tượng;<br>3. Tính lương khai thác, khách hàng mới, lương cứng, lương khoán hoàn thành KPI:<br>- Bổ sung luồng tính toán;<br>- Bổ sung vào chức năng Quản lý nghiệp vụ để thiết lập quy tắc tính;<br>- Bổ sung vào các chức năng tra cứu lương trên app & web;<br>4. Bổ sung chức năng Quản lý dữ liệu để nhập các thông số phục vụ tính lương:<br>- Bưu cục: Doanh thu kế hoạch trước & sau thuế;<br>- Nhân viên: Số ngày nghỉ, tỉ lệ hoàn thành KPI cá nhân, HRL, bước lương;<br>5. Bổ sung Báo cáo Tỷ lệ hoàn thành doanh thu.|

<div class="page"></div>

MỤC LỤC

# GIỚI THIỆU
## Mục đích của tài liệu

Tài liệu đặc tả các hệ thống tính lương SCS Metfone.

## Phạm vi

Hệ thống SCS Metfone.

## Thuật ngữ và chữ viết tắt
## Tài liệu tham chiếu

| # | # | # | # |
|---|---|---|---|
|STT|Tên tài liệu|Người biên soạn|Địa chỉ|
|||||
|||||
|||||
|||||

# PHÂN TÍCH VÀ THIẾT KẾ SƠ BỘ
## Sơ đồ quan hệ thực thể

<img src="media/image5.png" id="image1">

## Phân rã chức năng

| # | # | # |
|---|---|---|
|ID|Chức năng|Ưu tiên|
|UC01|Đăng nhập|High|
|UC02|Đăng xuất|High|
|UC03|Đẩy sự kiên giao/nhận/kết nối|High|
|UC04|Đồng bộ cây tổ chức (nhân viên, bưu cục, chi nhánh)|High|
|UC05|Danh sách phần tử lương|Medium|
|UC06|Danh sách phiên bản|Medium|
|UC07|Thêm phiên bản|Medium|
|UC08|Sửa phiên bản|Medium|
|UC09|Xóa phiên bản|Medium|
|UC10|Tính thử phiên bản|Medium|
|UC11|Đề xuất phiên bản|Medium|
|UC12|Phê duyệt phiên bản|Medium|
|UC13|Danh sách lượt nhập liệu|Medium|
|UC14|Nhập liệu|Medium|
|UC15|Xóa lượt nhập liệu|Medium|
|UC16|Đề xuất lượt nhập liệu|Medium|
|UC17|Phê duyệt lượt nhập liệu|Medium|
|UC18|Tự động kích hoạt & bất hoạt phiên bản|Medium|
|UC19|Tính lương theo sự kiện|High|
|UC20|Báo cáo tổng hợp thù lao nhân viên|High|
|UC21|Báo cáo hoa hồng đại lý|High|
|UC22|Tra cứu thu nhập của bản thân trên app bưu tá metfone|Medium|

# THIẾT KẾ CHI TIẾT CHỨC NĂNG
## Quản lý người dùng 
### Đăng nhập

| # | # |
|---|---|
|Use Case|Đăng nhập|
|Use Case ID|UC01|
|Description|Cho phép người dùng xác thực qua SSO thị trường để truy cập web SCS.|
|Actor|Người dùng;<br>Web SCS;<br>SSO thị trường.|
|Pre-Condition|Đã cấu hình client với SSO thị trường;<br>Người dùng có tài khoản hợp lệ.|
|Trigger|Người dùng muốn truy cập vào web SCS.|
|Post-Condition|Web SCS nhận được token & cho phép người dùng sử dụng các chức năng tùy vai trò.|
|Priority|High|
|Main Flow|1. User truy cập web SCS;<br>2. N – Chưa có phiên hợp lệ;<br>3. Ridirect sang trang đăng nhập của SSO thị trường;<br>4. SSO hiển thị form đăng nhập;<br>5. User nhập username & password hợp lệ & gửi;<br>6. Y – SSO xác thực thành công;<br>7. Web SCS lấy token, lưu token an toàn, decode lấy thông tin user;<br>8. Web SCS điều hướng về trang đích và cho phép user truy cập tài nguyên.<br>Use Case hoàn thành.|
|Alternative Flow|2. Y – Đã có phiên hợp lệ.<br>Use Case tiếp tục ở bước 8.|
|Exception Flow|6. N – SSO xác thực không thành công.<br>Use Case kết thúc.|

### Đăng xuất

| # | # |
|---|---|
|Use Case|Đăng xuất|
|Use Case ID|UC02|
|Description|Cho phép người dùng kết thúc phiên làm việc trên web SCS và trên SSO thị trường, đảm bảo không thể truy cập lại tài nguyên được bảo vệ mà không đăng nhập lại.|
|Actor|Người dùng;<br>Web gán nhãn;<br>SSO thị trường.|
|Pre-Condition|Đã cấu hình client với SSO thị trường;<br>Người dùng đang có phiên đăng nhập.|
|Trigger|Người dùng muốn đăng xuất khỏi web SCS.|
|Post-Condition|Tất cả phiên SSO của người dùng bị hủy.<br>Token trong ứng dụng bị xóa.<br>Người dùng quay về trang “Đăng nhập”|
|Priority|High|
|Main Flow|User chọn “Đăng xuất”;<br>Web SCS xóa token đang lưu;<br>Web SCS ridirect tới SSO;<br>SSO hủy phiên người dùng;<br>SSO chuyển người dùng về màn đăng nhập.<br>Use Case hoàn thành.|

## Tổng hợp dữ liệu
###  Sự kiện tính lương
#### Sự kiện giao & nhận hàng

Mỗi bản tin trong topic kafka có kiểu dữ liệu là sting và theo cấu trúc json

Thời gian đẩy: realtime.

| # | # | # | # | # | # |
|---|---|---|---|---|---|
|STT|Tên tham số|Topic giao hàng<br>Bao gồm các sự kiện giao thành công (TT501) lần đầu tiên của đơn (không tính đơn tách kiện)||Topic nhận hàng<br>Bao gồm các sự kiện nhận thành công (TT200) lần đầu tiên của đơn (không tính đơn tách kiện).||
|||key:value Json|Ghi chú|key:value Json|Ghi chú|
|1|Địa điểm giao/nhận|receiveType:string|AT_STORE: tại cửa hàng<br>AT_HOME: tại nhà|receiveType:string|AT_STORE: tại cửa hàng<br>AT_HOME: tại nhà|
|2|Mã phiếu gửi.|orderId:string|Mã vận đơn|orderId: string||
|3|Trạng thái|status:string|501|status:string|200|
|4|Mã dịch vụ chính|mainServiceCode:string|Mã dịch vụ chính của đơn. (main)|mainServiceCode:string|Mã dịch vụ chính của đơn. (main)|
|5|Mã dịch vụ khác|otherServiceCode:string|Danh sách các mã dịch vụ khác của đơn.|otherServiceCode:string|Danh sách các mã dịch vụ khác của đơn.|
|6|Trọng lượng|totalWeight:float|Đơn vị: gram<br>Tổng trọng lượng trong các items|totalWeight:float|Đơn vị: gram<br>Tổng trọng lượng trong các items|
|8|Tổng cước trước thuế|totalFees: float|Tổng cước trước thuế|totalFees: float|Tổng cước trước thuế|
|9|Tổng cước sau thuế|totalFeesVAT: float|Tổng cước sau thuế|totalFeesVAT: float|Tổng cước sau thuế|
|10|Tiền thu hộ|cod:float|Tiền thu hộ của đơn|cod:float|Tiền thu hộ của đơn|
|11|Bưu cục gốc|receivePostCode:string|Mã bưu cục gốc.<br>→ Có thể NULL|receivePostCode: string|Mã bưu cục gốc.<br>→ Có thể NULL|
|12|Loại Bưu cục của BC gốc|receivePostCodeType:string|POST: Bưu cục<br>AGENT: Đại lý ủy quyền|receivePostCodeType:string|POST: Bưu cục<br>AGENT: Đại lý ủy quyền|
|13|Bưu cục phát|deliveryPostcode:string|Mã bưu cục phát dự kiến.<br>→ Có thể NULL|deliveryPostcode: string|Mã bưu cục phát dự kiến.<br>→ Có thể NULL|
|14|Loại bưu cục của Bưu cục phát&nbsp;|deliveryPostcodeType:string|POST: Bưu cục<br>AGENT: Đại lý ủy quyền|deliveryPostcodeType:string|POST: Bưu cục<br>AGENT: Đại lý ủy quyền|
|15|Loại hàng hóa (Hàng; Thư; Kiện)|parcelType:string|Mục đích xác định hàng<br>GOODS: Hàng<br>DOCUMENT: Thư|parcelType: string&nbsp;|GOODS: Hàng<br>DOCUMENT: Thư|
|16|Mã KH gửi|customerID:string|Mã của khách hàng gửi.<br>→ Có thể NULL|customerID:string|Mã của khách hàng gửi.|
|17|Thời gian tác động|updatedAt:bigint|Thời gian đơn hàng được chuyển lên TT501 lần đầu tiên.|updatedAt: bigint|Thời gian đơn hàng được chuyển lên TT200 lần đầu tiên.|
|18|Userid tác động thực tế|userId:string|User_id chuyển đơn lên TT501 lần đầu tiên.|userId: string|User_id chuyển đơn lên TT200 lần đầu tiên.|
|19|Mã nhân viên&nbsp;giao thành công/nhận thành công thực tế|staffCode:string|Mã nhân viên của userid (21).|staffCode: string|Mã nhân viên của userid&nbsp;(21).|
|20|Bưu cục&nbsp;giao thành công/nhận thành công thực tế|postcodeStaff:string|Bưu cục trực thuộc của userid&nbsp;(21).<br>Hiểu là Bưu cục mà user thuộc và thực hiện hoạt động giao thành công|postcodeStaff: string|Bưu cục trực thuộc của userid&nbsp;(21).<br>Hiểu là Bưu cục mà user thuộc và thực hiện hoạt động nhận thành công|
|21|Loại của&nbsp;Bưu cục&nbsp;giao thành công/nhận thành công thực tế|postcodeStaffType:string|POST: Bưu cục<br>AGENT: Đại lý ủy quyền|postcodeStaffType:string|POST: Bưu cục<br>AGENT: Đại lý ủy quyền|
|22|Userid người giới thiệu|userIdReferrer:string|Userid chuyển đơn lên TT501 lần đầu tiên.|userIdReferrer: string|Userid chuyển đơn lên TT200 lần đầu tiên.|
|23|Mã nhân viên&nbsp;người giới thiệu|staffCodeReferrer:string|Mã nhân viên của userid (21).|staffCodeReferrer: string|Mã nhân viên của userid&nbsp;(21).|

#### Sự kiện hoàn thành chuyến xe

06.04.2026 – Bổ sung sự kiện hoàn thành chuyến xe

Thời điểm:

Ngày 20 tháng n → Chốt dữ liệu kỳ 1-15 tháng n;

Ngày 3 tháng n+1 → Chốt dữ liệu kỳ 15 – ngày cuối tháng n;

Bao gồm các chuyến xe thỏa mãn:

Thời gian kết thúc thuộc kỳ;

| # | # | # | # |
|---|---|---|---|
|STT|Tên tham số|Topic thông tin chuyến xe||
|||key:value Json|Ghi chú|
|1|Mã chuyến xe|tripCode:string|Mã chuyến xe.<br>VD. CX005238490.|
|2|Đơn vị vận chuyển|organizationCode:string|Mã đơn vị vận chuyển (bưu cục).<br>VD. TN2.|
|3|Mã hành trình|routeCode:string|Mã hành trình.<br>VD. XHH1643.|
|4|Mã loại hành trình|routeTypeCode:string|Mã loại hành trình.<br>VD. LHT000006|
|5|Loại hành trình|routeTypeName:string|Tên loại hành trình.<br>VD. Nội tỉnh|
|6|Chiều đi|direction:string|Phân biệt chiều đi & chiều về, bao gồm:<br>1 – Chiều đi;<br>2 – Chiều về.|
|7|Tên tuyến|roadName:string|Tên tuyến.<br>VD. NT-KGG.GOQUAO-05H00-CS|
|8|Biển số xe|vehiclePlate:string|Biển số của phương tiện.<br>VD. 29KT-20115|
|9|Mã loại sở hữu|vehicleSourceCode:string|Mã loại phương tiện, bao gồm:<br>1 – Xe nội bộ;<br>2 – Xe khô;<br>3 – Xe nguyên chuyến.|
|10|Tên loại sở hữu|vehicleSourceName:string|Tên loại phương tiện.<br>VD. Xe nguyên chuyến.|
|11|Mã loại phương tiện|vehicleTypeCode:string|Mã loại phương tiện.|
|12|Tên loại phương tiện|vehicleTypeName:string|Tên loại phương tiện.|
|13|Đối tác|partnerName:string|Tên đối tác (VD. HỘ KINH DOANH MINH QUÂN). DT00118|
|14|Khối lương hàng hóa|weight:float|Khối lượng của hàng hóa trên xe (Đơn vị:kg).<br>VD. 5299.49|
|15|Trọng tải xe|capacity:float|Trọng tải xe (Đơn vị:kg).<br>VD. 3500|
|16|Hiệu quả xe|efficiency:float|Tỷ lệ hiệu quả xe (Đơn vị: %).<br>VD. 151.41|
|17|Sản lượng tải|bagVolume:float|Số lượng tải trên xe (Đơn vị: Tải).<br>VD. 465|
|18|Sản lượng kiện|packageVolume:float|Số lượng kiện trên xe (Đơn vị: Kiện).<br>VD. 54|
|19|Trọng lượng tải|bagWeight:float|Trọng lượng tải trên xe (Đơn vị: kg).<br>VD. 4526,90|
|20|Trọng lượng kiện|packageWeight:float|Trọng lượng kiện trên xe (Đơn vị: kg).<br>VD. 772,58|
|21|Thời gian khởi hành|startTime:bigInt|Thời gian chuyến xe khởi hành, định dạng timestamp miliseconds.|
|23|Thời gian kết thúc|endTime:bigInt|Thời gian chuyến xe kết thúc, định dạng timestamp miliseconds.|
|24|Danh sách tài xế|drivers:list|Danh sách tài xế của chuyến xe (hiện mỗi chuyến có 2 tài xế, danh sách có thể bị sửa đổi), mỗi tài xế lấy ra:<br>userId:string – Định danh user của tài xế;<br>postcode:string – Mã bưu cục của tài xế;<br>jobTitle:string – Mã chức danh của tài xế.|
|25|Km hành trình.|plannedDistance:float|Số km do người vận hành tạo hành trình nhập.|
|26|Km tài xế nhập.|reportedDistance:float|Số km do tài xế nhập.|
|27|Km GPS|actualDistance:float|Số km GPS.|
|28|Loại km được phê duyệt|approvedDistanceType:string|Loại km được phê duyệt, bao gồm:<br>“PLANNED”;<br>“REPORTED”;<br>“GPS”.|

#### Sự kiện khách hàng mới

Thời điểm: XX:XX ngày 3 tháng n+1;

Bao gồm: Toàn bộ khách hàng thỏa mãn:

Thời gian có đơn được nhập doanh thu lần đầu tiên nằm trong 6 tháng đổ lại;

Có ít nhất 01 đơn được nhập doanh thu trong tháng n;

Mỗi khách hàng lấy ra các thông tin sau:

| # | # | # | # |
|---|---|---|---|
|STT|Tên tham số|Topic thông tin khách hàng mới||
|||key:value Json|Ghi chú|
|1|ID Khách hàng|cusId:string|ID Khách hàng.|
|2|Tháng khoán|reportMonth:string|Tháng báo cáo, định dạng MMYYYY.|
|2|Tên khách hàng|cusName:string|Họ và tên đầy đủ của khách hàng.|
|3|Ngày phát sinh doanh thu đầu tiên|firstRevDate:date|Ngày đầu tiên khách hàng có đơn hàng được nhập doanh thu thành công.|
|4|Số tháng doanh thu|RevMonths:float|Số tháng tính từ ngày phát sinh doanh thu, được tính như sau:<br>Tháng hiện tại – Tháng phát sinh doanh thu + 1<br>VD. Khách phát sinh doanh thu lần đầu vào 23/01/2026, tháng n là tháng 04/2026 → Số tháng doanh thu = 4 tháng.|
|5|Doanh thu tháng phát sinh|firstMonthRev:float|Tổng doanh thu của khách hàng vào tháng chứa ngày phát sinh doanh thu lần đầu tiên.|
|6|Doanh thu tháng hiện tại|monthRev:float|Tổng doanh thu của khách hàng vào tháng n.|
|7|Giảm giá, chiết khấu|monthDisc:float|Tổng giảm giá, chiết khấu của khách hàng vào tháng n.|
|8|Nhân viên giới thiệu|userIdReferrer:string|ID Nhân viên giới thiệu.|

### Đồng bộ cây tổ chức (nhân viên/bưu cục/chi nhánh)
#### Thông tin nhân sự

06.04.2026 – Nâng tần suất đồng bộ + Điều chỉnh thiết kế bản tin thông tin nhân sự

Thời điểm: Khi phát sinh thêm mới / điều chỉnh thông tin của 1 kết hợp user + bưu cục;

Bao gồm: Các kết hợp user + bưu cục.

| # | # | # | # |
|---|---|---|---|
|STT|Tên tham số|TOPIC_NHANSU_CHITIET||
|||key:value Json|Ghi chú|
|1|Userid&nbsp;|userId:string|Id nhân viên|
|2|Mã nhân viên&nbsp;tạo tải thực tế|staffCode:string|Mã nhân viên của userid tạo tải thực tế.|
|3|username nhân viên|username||
|4|điện thoại|phone||
|5|trạng thái|status|ACTIVE<br>OFF|
|6|họ|firstname||
|7|tên|lastname||
|8|Họ và tên|fullname||
|9|Bưu cục|department_ID|Bưu cục trực thuộc|
|10|ngày tạo|createdAt:bigint|Ngày tạo của kết hợp user + bưu cục.|
|11|Chức danh|jobTitle: string|Chức danh của kết hợp user + bưu cục (VD. Nhân viên lái xe,…)|
|12|Loại hợp đồng|employeeGroup: string|Loại đối tượng của user (VD. Hợp đồng lao động, CTV,…)|

#### Thông tin chi nhánh

06.04.2026 – Nâng tần suất đồng bộ lên real-time.

Khi có cập nhật thêm mới/điều chỉnh  → Global gửi kafka. 

| # | # | # | # |
|---|---|---|---|
|STT|Tên tham số|TOPIC_CHINHANH_CHITIET||
|||key:value Json|Ghi chú|
|1|id|departmentId:string|Id chi nhánh|
|2|Mã chi nhánh|Code:string|Mã chi nhánh|
|3|Tên chi nhánh|name|Tên chi nhánh|
|4|điện thoại|phone||
|5|trạng thái|status|ACTIVE<br>OFF|
|6|Người tạo|userID|userID người tạo|
|7|ngày tạo|createdAt||
|8|địa chỉ|formattedAddress||

#### Thông tin bưu cục đại lý

06.04.2026 – Nâng tần suất đồng bộ lên real-time.

Khi có cập nhật thêm mới/điều chỉnh  → Global gửi kafka. 

15.05.2026 – Thêm quốc gia, tỉnh, huyện, xã

| # | # | # | # |
|---|---|---|---|
|STT|Tên tham số|TOPIC_BUUCUC_CHITIET||
|||key:value Json|Ghi chú|
|1|id|departmentId:string|Id bưu cục/ đại lý|
|2|id chi nhánh|departmentParentId|id của chi nhánh mà Bưu cục/ đại lý thuộc|
|3|Mã Bưu cục/đại lý|Code:string|Mã chi nhánh|
|4|Tên&nbsp;Bưu cục/đại lý|name|Tên chi nhánh|
|5|Loại|type|POST: Bưu cục<br>AGENT: Đại lý ủy quyền|
|6|Trưởng bưu cục|hpo_username||
|7|điện thoại|phone||
|8|trạng thái|status|ACTIVE<br>OFF|
|9|Người tạo|userID|userID người tạo|
|10|Ngày tạo|createdAt||
|11|Địa chỉ|formattedAddress||
|12|ID quốc gia|countryId:string||
|13|Mã quốc gia|countryCode:string||
|14|ID tỉnh/thành phố|provinceId:string||
|15|Mã tỉnh/thành phố|provinceCode:string||
|16|ID quận/huyện|districtId:string||
|17|Mã quận/huyện|districtCode:string||
|18|ID phường/xã|wardId:string||
|19|Mã phường/xã|wardCode:string||

#### Thông tin chức danh

25.04.2026 – Đồng bộ thêm danh mục chức danh

| # | # | # | # |
|---|---|---|---|
|STT|Tên tham số|Thông tin chức danh||
|||key:value Json|Ghi chú|
|1|id|jobTitleId:string|Id chức danh.|
|2|Mã chức danh|jobTitleCode:string|Mã chức danh.|
|3|Tên chức danh|jobTitleName:string|Tên chức danh.|

#### Thông tin nhóm đối tượng

25.04.2026 – Đồng bộ thêm danh mục đối tượng

| # | # | # | # |
|---|---|---|---|
|STT|Tên tham số|Thông tin chức danh||
|||key:value Json|Ghi chú|
|1|id|empGroupId:string|Id nhóm đối tương.|
|2|Mã đối tượng|empGroupCode:string|Mã nhóm đối tượng.|
|3|Tên đối tượng|empGroupName:string|Tên nhóm đối tượng.|

#### Thông tin quốc gia

15.05.2026 – Thêm quốc gia

| # | # | # | # |
|---|---|---|---|
|STT|Tên tham số|Thông tin chức danh||
|||key:value Json|Ghi chú|
|1|id|country_id:string|ID Quốc gia (Khóa chính)|
|2|Mã quốc gia|code:string||
|3|Tên đầy đủ|name:string||
|4|Tên ngắn|short_name:string||
|5|Tên quốc gia bằng tiếng Anh|name_en:string||
|6|Trạng thái|status:string|Trạng thái: ACTIVE / INACTIVE (mặc định là INACTIVE).|
|7|Thời gian tạo|created_at:bigint||
|8|Thời gian cập nhật|updated_at:bigint||
|9|ID Người tạo|created_by:string||
|10|Thông tin thêm về người tạo|created_by_info:json||
|11|ID Người cập nhật|updated_by:string||
|12|Thông tin thêm người cập nhật|updated_by_info: json||

#### Thông tin tỉnh/thành phố

15.05.2026 – Thêm tỉnh/thành phố

| # | # | # | # |
|---|---|---|---|
|STT|Tên tham số|Thông tin chức danh||
|||key:value Json|Ghi chú|
|1|Id|province_id:string||
|2|ID Quốc gia|country_id:string||
|3|Mã quốc gia|country_code:string||
|4|Mã tỉnh|code:string||
|5|Tên tỉnh|name:string||
|6|Tên ngắn|short_name:string||
|7|Tên tiếng Anh|name_en:string||
|8|Thông tin mở rộng|properties:json||
|9|Trạng thái|status:string|Trạng thái: ACTIVE / INACTIVE (mặc định là INACTIVE).|
|10|Thời gian tạo|created_at:bigint||
|11|Thời gian cập nhật|updated_at:bigint||
|12|ID Người tạo|created_by:string||
|13|Thông tin thêm về người tạo|created_by_info:json||
|14|ID Người cập nhật|updated_by:string||
|15|Thông tin thêm người cập nhật|updated_by_info: json||

#### Thông tin quận/huyện

15.05.2026 – Thêm quận/huyện

| # | # | # | # |
|---|---|---|---|
|STT|Tên tham số|Thông tin chức danh||
|||key:value Json|Ghi chú|
|1|Id|district_id:string||
|2|Id quốc gia|country_id:string||
|3|Mã quốc gia|country_code:string||
|4|ID tỉnh/thành phố|province_id:string||
|5|Mã tỉnh/thành phố|province_code:string||
|6|Mã quận/huyện|code:string||
|7|Tên quận/huyện đầy đủ|name:string||
|8|Tên quận/huyện rút gọn|short_name:string||
|9|Tên quận/huyện tiếng Anh|name_en:string||
|10|Trạng thái|status:string|Trạng thái: ACTIVE / INACTIVE (mặc định là INACTIVE).|
|11|Thời gian tạo|created_at:bigint||
|12|Thời gian cập nhật|updated_at:bigint||
|13|ID Người tạo|created_by:string||
|14|Thông tin thêm về người tạo|created_by_info:json||
|15|ID Người cập nhật|updated_by:string||
|16|Thông tin thêm người cập nhật|updated_by_info: json||

#### Thông phường/xã

15.05.2026 – Thêm phường/xã

| # | # | # | # |
|---|---|---|---|
|STT|Tên tham số|Thông tin chức danh||
|||key:value Json|Ghi chú|
|1|ID|ward_id:string||
|2|ID quốc gia|country_id:string||
|3|Mã quốc gia|country_code:string||
|4|ID tỉnh/thành phố|province_id:string||
|5|Mã tỉnh/thành phố|province_code:string||
|6|ID quận huyện|district_id:string||
|7|Mã quận huyện|district_code:string||
|8|Mã phường xã|code:string||
|9|Tên phường xã|name:string||
|10|Tên phường xã rút gọn|short_name:string||
|11|Tên|name_en:string||
|12|Trạng thái|status:string|Trạng thái: ACTIVE / INACTIVE (mặc định là INACTIVE).|
|13|Thời gian tạo|created_at:bigint||
|14|Thời gian cập nhật|updated_at:bigint||
|15|ID Người tạo|created_by:string||
|16|Thông tin thêm về người tạo|created_by_info:json||
|17|ID Người cập nhật|updated_by:string||
|18|Thông tin thêm người cập nhật|updated_by_info: json||

## Thiết lập nghiệp vụ tính lương
### Chức năng web SCS
#### Quản lý quy tắc tính lương
##### Danh sách phần tử lương

18.04.2026 Điều chỉnh danh sách phần tử lương

25.04.2026 Điều chỉnh danh sách sự kiện & phần tử lương.

| # | # |
|---|---|
|Use Case|Danh sách phần tử lương|
|Use Case ID|UC2.2.1|
|Description|Cho phép xem danh sách phần tử lương.|
|Actor|Primary Actor(s): Nhân viên khai giá; Quản lý giá<br>Secondary Actor(s):&nbsp;Admin hệ thống|
|Pre-Condition|User đăng nhập thành công vào web SCS.|
|Trigger|SCS → Quản lý nghiệp vụ|
|Post-Condition|Xem được danh sách phần tử lương.|
|Priority|Medium|
|Business Rule|BR01. Kiểm tra tính hợp lệ của bộ lọc.<br>(BL1) Từ khóa: Chuỗi 0-255 ký tự, không chứa khoảng cách đầu cuối;<br>(BL2) Đối tượng: Chọn 1 trong danh sách gồm:<br>Nhân viên;<br>Đại lý.<br>(BL3) Loại lương: Chọn 1 trong danh sách gồm:<br>Phát triển;<br>Khai thác;<br>Nhận<br>Giao;<br>KPI.<br>(BL4) Sự kiện: Chọn 1 trong danh sách<br>Nhận hàng;<br>Giao hàng;<br>Kết nối;<br>Chốt thù lao kết nối ngày;<br>Chốt doanh thu nhận tháng;<br>Chốt doanh thu giao tháng.<br>Khách hàng mới;<br>Khai thác;<br>Chốt KPI;<br>Chốt lương cứng.<br>(BL5) Hình thức tính toán: Chọn 1 trong danh sách bao gồm:<br>Tự động;<br>Thủ công;<br>BR02. Lấy ra tất cả phần tử lương t/m tất cả các điều kiện sau, điều kiện nào để trống thì coi như thỏa mãn:<br>Có tên chứa từ khóa được nhập vào tại (BL1) không phân biệt hoa thường, dấu;<br>Đối tượng = (BL2);<br>Loại lương = (BL3);<br>Sự kiện tính = (BL4);<br>Hình thức tính toán = (BL5).<br>BR03. Cột hiển thị, chọn 1 hoặc nhiều cột để hiển thị, bao gồm:<br>STT;<br>Tên phần tử;<br>Mã phần tử;<br>Đối tượng;<br>Hình thức;<br>Sự kiện;<br>Tên file quy tắc hiện hành → Chọn để tải xuống file .xlsx;<br>Mã phiên bản;<br>Thời gian cập nhật;<br>Người cập nhật;<br>Thao tác:<br>Nếu hình thức thanh toán = “Tự động” → Xem chi tiết → Chuyển sang màn danh sách phiên bản;<br>Nếu hình thức thanh toán = “Thủ công” → Xem chi tiết → Chuyển sang màn danh sách lượt nhập liệu.<br>BR04. Sắp xếp: Chọn 1 trong các lựa chọn:<br>Theo tên phần tử (A→Z);<br>Theo mã phần tử (A→Z);<br>Theo thời gian cập nhật (mới → cũ).<br>BR05. Phân trang: 10 bản ghi/trang.|

<img src="media/image6.png" id="image2">

| # | # | # | # | # | # | # |
|---|---|---|---|---|---|---|
|STT|Đối tượng|Tên phần tử|Mã phần tử|Sự kiện|Phân loại cấp 1|Hình thức|
|1|Nhân viên|Lương cứng|EmpBaseFee|Chốt lương cứng|Lương cứng|Tự động|
|2|Nhân viên|Thù lao hoàn thành KPI|EmpKpiFee|Chốt KPI|Lương khoán > Hoàn thành KPI|Tự động|
|3|Nhân viên|Thù lao sản lượng nhận|EmpBasePickupFee|Nhận hàng|Lương khoán > Nhận hàng|Tự động|
|4|Nhân viên|Thù lao trọng lượng vượt nhận|EmpWeightPickupFee|Nhận hàng|Lương khoán > Nhận hàng|Tự động|
|5|Nhân viên|Thù lao sản lượng giao|EmpBaseDeliveryFee|Giao hàng|Lương khoán > Giao hàng|Tự động|
|6|Nhân viên|Thù lao trọng lượng vượt giao|EmpWeightDeliveryFee|Giao hàng|Lương khoán > Giao hàng|Tự động|
|7|Nhân viên|Thù lao khai thác|EmpHandlingFee|Khai thác|Lương khoán > Khai thác|Tự động|
|8|Nhân viên|Thù lao kết nối|EmpTransportFee|Hoàn thành chuyến xe|Lương khoán > Kết nối|Tự động|
|9|Nhân viên|Thù lao khách hàng mới|EmpCustomer-DevelopmentFee|Khách hàng mới|Khách hàng mới|Tự động|
|10|Nhân viên|Phụ cấp|EmpAllowance|-|Phụ cấp|Thủ công|
|11|Nhân viên|Thưởng|EmpBonus|-|Thưởng phạt|Thủ công|
|12|Nhân viên|Phạt|EmpPenalty|-|Thưởng phạt|Thủ công|
|13|Đại lý|Thù lao nhận (Tạm tính)|AgtPickupFee|Nhận hàng|Hoa hồng nhận|Tự động|
|14|Đại lý|Điều chỉnh thù lao nhận|AgtPickupFeeAdjustment|Chốt thù lao cuối tháng|Hoa hồng nhận|Tự động|
|15|Đại lý|Thù lao giao|AgtDeliveryFee|Giao hàng|Hoa hồng giao|Tự động|

##### Danh sách phiên bản

13.04.2026 Hiển thị button “Sửa” ở tất cả trạng thái;

| # | # |
|---|---|
|Use Case|Danh sách phiên bản|
|Use Case ID|UC2.2.2|
|Description|Cho phép người dùng xem danh sách phiên bản của 1 phần tử lương.|
|Actor|Primary Actor(s): Nhân viên khai giá; Quản lý giá<br>Secondary Actor(s):&nbsp;Admin hệ thống|
|Pre-Condition|User đăng nhập thành công vào web SCS;<br>Phần tử lương có hình thức tính là “Tự động”;|
|Trigger|SCS → Quản lý quy tắc nghiệp vụ → Chọn xem chi tiết 1 phần tử.|
|Post-Condition|Người dùng xem được danh sách phiên bản quy tắc tính của 1 phần tử.|
|Priority|Medium|
|Business Rule|BR01. Kiểm tra tính hợp lệ của bộ lọc.<br>(BL1) Phần tử: Phần tử đã chọn xem chi tiết ở use case “Danh sách phần tử lương”;<br>(BL2) Thời gian: Từ ngày (hh:mm dd/mm/yyyy) – Đến ngày (hh:mm dd/mm/yyyy);<br>BR02. Quy tắc tìm kiếm:<br>Lấy ra danh sách version thỏa mãn, tiêu chí nào bỏ trống thì coi như thỏa mãn:<br>Thuộc phần tử lương (BL1);<br>Thời gian áp dụng giao với (BL2);<br>BR03. Cột hiển thị, chọn 1 hoặc nhiều cột để hiển thị, bao gồm:<br>STT;<br>Mã phiên bản;<br>Tên file quy tắc → Chọn để tải xuống file .xlsx;<br>Ngày bắt đầu áp dụng;<br>Ngày ngưng áp dụng;<br>Ngày cập nhật;<br>Người cập nhật;<br>Tên trạng thái;<br>Ghi chú;<br>Thao tác riêng:<br>Trạng thái “Soạn thảo”: Sửa; Xóa; Tính thử; Lên lịch;<br>Trạng thái “Chờ duyệt”: Sửa; Tính thử; Phê duyệt;<br>Trạng thái “Đã từ chối”: Sửa; Xóa; Tính thử; Lên lịch;<br>Trạng thái “Đã lên lịch”: Sửa; Tính thử;<br>Trạng thái “Hiện hành”: Sửa; Tính thử;<br>Trạng thái “Đã dừng”: Sửa; Tính thử;<br>BR04. Sắp xếp: Chọn 1 trong các lựa chọn:<br>Thời gian cập nhật (mới → cũ);<br>BR05. Phân 10 dòng / trang.|

<img src="media/image7.png" id="image3">

##### Thêm phiên bản

| # | # |
|---|---|
|Use Case|Thêm phiên bản|
|Use Case ID|UC2.2.3|
|Description|Cho phép người dùng thêm 1 phiên bản quy tắc tính cho phần tử lương.|
|Actor|Primary Actor(s): Nhân viên khai giá; Quản lý giá<br>Secondary Actor(s):&nbsp;Admin hệ thống|
|Pre-Condition|User đăng nhập thành công vào web SCS.|
|Trigger|SCS → Quản lý quy tắc nghiệp vụ → Chọn xem chi tiết 1 nghiệp vụ → Chọn thao tác chung “Thêm mới”|
|Post-Condition|Thêm thành công phiên bản;|
|Priority|Medium|
|Business Rule|BR_01_01: Kiểm tra định dạng & quy tắc nghiệp vụ:<br>(1) Phần tử giá: Tự động lấy phần tử giá của rule set đang xét;<br>(2) Mã phiên bản: Nhập chuỗi chỉ chứa chữ in hoa không dấu, số và ký tự “_”, tối đa 255 ký tự;<br>(3) Excel: Bắt buộc, định dạng .xlsx, kích thước tối đa (???).<br>(4) DRL: Bắt buộc, tự động convert từ (3), hợp lệ khi không xảy ra lỗi khi convert.<br>(5) Ngày bắt đầu: Bắt buộc, chọn giờ chẵn HH dd/mm/yyyy, ngày bắt đầu phải lớn hơn nhày hiện tại;<br>(6) Ngày kết thúc: Bắt buộc, chọn giờ chẵn HH dd/mm/yyyy, ngày kết thúc phải lớn hơn ngày bắt đầu và lớn hơn ngày hiện tại;<br>(7) Ghi chú: Không bắt buộc, chuỗi 1-1000 ký tự, không chứa khoảng trắng đầu cuối.<br>(8) Trạng thái = “Soạn thảo”;<br>Tự động ghi nhận người, ngày tạo & cập nhật.<br>BR_01_02: Kiểm tra phân quyền&nbsp;→ Tham chiếu phụ lục phân quyền.<br>BR_01_03: Phản hồi kết quả cho người dùng&nbsp;→ Tham chiếu phụ lục message.<br>BR_01_04: Nếu đang nhập dở thông tin mà thoát&nbsp;→ Yêu cầu người dùng xác nhận hủy thông tin đang nhập dở.|

<img src="media/image8.png" id="image4">

##### Sửa phiên bản

18.04.2026 Cho phép sửa ở trạng thái chờ lên lịch & hiện hành.

| # | # |
|---|---|
|Use Case|Sửa phiên bản|
|Use Case ID|UC2.2.3|
|Description|Cho phép người dùng sửa 1 phiên bản quy tắc tính của phần tử lương.|
|Actor|Primary Actor(s): Nhân viên khai giá; Quản lý giá<br>Secondary Actor(s):&nbsp;Admin hệ thống|
|Pre-Condition|User đăng nhập thành công vào web SCS.|
|Trigger|SCS → Quản lý quy tắc nghiệp vụ → Chọn xem chi tiết 1 phần tử → Chọn thao tác riêng “Chỉnh sửa”|
|Post-Condition|Sửa thành công phiên bản;|
|Priority|Medium|
|Business Rule|BR_01_01: Lấy ra thông tin chi tiết & điền sẵn, cho phép người dùng điều chỉnh theo quy tắc sau:<br>(1) Phần tử giá: KHÔNG chỉnh sửa;<br>(2) Mã phiên bản: <br>Chỉ sửa ở trạng thái “Soạn thảo” & “Đã từ chối”;<br>Nhập chuỗi chỉ chứa chữ in hoa không dấu, số và ký tự “_”, tối đa 255 ký tự;<br>(3) Excel:<br>Chỉ sửa ở trạng thái “Soạn thảo” & “Đã từ chối”;<br>Bắt buộc, định dạng .xlsx, kích thước tối đa (???).<br>(4) DRL:<br>Chỉ sửa ở trạng thái “Soạn thảo” & “Đã từ chối”;<br>Bắt buộc, tự động convert từ (3), hợp lệ khi không xảy ra lỗi khi convert.<br>(5) Ngày bắt đầu:<br>Chỉ sửa ở trạng thái “Soạn thảo”, “Đã từ chối”, “Chờ duyệt”;<br>Bắt buộc, chọn giờ chẵn HH dd/mm/yyyy, ngày bắt đầu phải lớn hơn nhày hiện tại;<br>(6) Ngày kết thúc:<br>Sửa ở tất cả các trạng thái;<br>Bắt buộc, chọn giờ chẵn HH dd/mm/yyyy, ngày kết thúc phải lớn hơn ngày bắt đầu và lớn hơn ngày hiện tại;<br>(7) Ghi chú:<br>Chỉ sửa ở trạng thái “Soạn thảo”, “Đã từ chối”, “Chờ duyệt”;<br>Không bắt buộc, chuỗi 1-1000 ký tự, không chứa khoảng trắng đầu cuối.<br>(8) Trạng thái: KHÔNG chỉnh sửa;<br>Tự động ghi nhận người, ngày cập nhật.<br>BR_01_02: Kiểm tra phân quyền&nbsp;→ Tham chiếu phụ lục phân quyền.<br>BR_01_03: Phản hồi kết quả cho người dùng&nbsp;→ Tham chiếu phụ lục message.<br>BR_01_04: Nếu đang nhập dở thông tin mà thoát&nbsp;→ Yêu cầu người dùng xác nhận hủy thông tin đang nhập dở.|

<img src="media/image9.png" id="image5">

##### Xóa phiên bản

| # | # |
|---|---|
|Use Case|Xóa phiên bản|
|Use Case ID|UC2.2.3|
|Description|Cho phép xóa 1 phiên bản.|
|Actor|Primary Actor(s): Nhân viên khai giá; Quản lý giá<br>Secondary Actor(s):&nbsp;Admin hệ thống|
|Pre-Condition|User đăng nhập thành công vào web SCS.|
|Trigger|SCS → Quản lý quy tắc nghiệp vụ → Chọn xem chi tiết 1 nghiệp vụ → Chọn thao tác riêng “Xóa”;|
|Post-Condition|Xóa thành công phiên bản.|
|Priority|Medium|
|Business Rule|Chỉ xóa ở trạng thái “Soạn thảo” & “Đã từ chối”.|

##### Tính thử phiên bản

18.04.2026 Điều chỉnh danh sách đầu vào

25.04.2026 Điều chỉnh danh sách đầu vào, bổ sung:

Số tháng phát sinh doanh thu

Doanh thu tháng hiện tại

Doanh thu tháng phát sinh

Giảm giá tháng hiện tại

Mã chức danh

Tỷ lệ hoàn thành doanh thu cá nhân

Tỷ lệ hoàn thành doanh thu trước thuế của bưu cục

Tỷ lệ hoàn thành doanh thu sau thuế của bưu cục

Tỷ lệ hoàn thành doanh thu trước thuế của tỉnh

Tỷ lệ hoàn thành doanh thu sau thuế của tỉnh

Tỷ lệ hoàn thành doanh thu trước thuế của vùng

Tỷ lệ hoàn thành doanh thu sau thuế của vùng

Tỷ lệ hoàn thành doanh thu tổng trước thuế

Tỷ lệ hoàn thành doanh thu tổng sau thuế

Số ngày nghỉ

| # | # |
|---|---|
|Use Case|Tính thử phiên bản|
|Use Case ID|UC2.2.6|
|Description|Cho phép tính thử kết quả 1 phiên bản.|
|Actor|Primary Actor(s): Nhân viên khai giá; Quản lý giá<br>Secondary Actor(s):&nbsp;Admin hệ thống|
|Pre-Condition|User đăng nhập thành công vào web SCS.|
|Trigger|SCS → Quản lý quy tắc nghiệp vụ → Chọn xem chi tiết 1 nghiệp vụ → Chọn thao tác riêng “Xóa”;|
|Post-Condition|Trả ra kết quả tính thử.|
|Priority|Medium|
|Business Rule|1. Nạp form nhập kịch bản tính thử: <br>Lấy ra danh sách tham số ảnh hưởng tới phần tử lương đang cần tính thử (Tham chiếu tới PL01. Tham số, vùng K7:R16);<br>Mỗi tham số lấy ra: Mã tham số & các giá trị tham chiếu nếu có (VD. Loại hàng hóa bao gồm “GOODS” và “DOCUMENT")<br>2. Hiển thị form nhập kịch bản tính thử;<br>3. Người dùng nhập kịch bản & chọn “Tính thử”;<br>4. Hệ thống tính thử theo kịch bản đã nhập;<br>4. Hệ thống trả ra kết quả tính thử, bao gồm:<br>Kết quả;<br>Quy tắc tính ra kết quả.|

<img src="media/image10.png" id="image6">

##### Đề xuất phiên bản

| # | # |
|---|---|
|Use Case|Đề xuất phiên bản|
|Use Case ID||
|Description|Cho phép người dùng đề xuất 1 phiên bản.|
|Actor|Primary Actor(s): Nhân viên khai giá; Quản lý giá<br>Secondary Actor(s):&nbsp;Admin hệ thống|
|Pre-Condition|User đăng nhập thành công vào web SCS.|
|Trigger|SCS → Quản lý quy tắc nghiệp vụ → Danh sách bộ quy tắc → Thao tác riêng “Đề xuất”|
|Post-Condition|Đề xuất phiên bản thành công.|
|Priority|Medium|
|Business Rule|Điều kiện:<br>Trạng thái của bộ quy tắc thuộc danh sách:<br>Soạn thảo;<br>Đã từ chối;<br>Thời gian bắt đầu > Thời gian hiện tại;<br>Kết quả đầu ra:<br>Chuyển bộ quy tắc sang trạng thái "Chờ duyệt";<br>Ghi nhận người & ngày cập nhật.|

<img src="media/image11.png" id="image7">

##### Phê duyệt phiên bản

18.04.2026 Nếu trùng thời gian hoạt động thì báo lỗi

| # | # |
|---|---|
|Use Case|Phê duyệt phiên bản|
|Use Case ID||
|Description|Cho phép người dùng phê duyệt 1 phiên bản.|
|Actor|Primary Actor(s): Quản lý giá<br>Secondary Actor(s):&nbsp;Admin hệ thống|
|Pre-Condition|User đăng nhập thành công vào web SCS.|
|Trigger|SCS → Quản lý quy tắc nghiệp vụ → Danh sách bộ quy tắc → Thao tác riêng “Phê duyệt”;|
|Post-Condition|Phê duyệt phiên bản thành công.|
|Priority|Medium|
|Business Rule|TH1: Đồng ý<br>Điều kiện:<br>Trạng thái của bộ quy tắc thuộc danh sách:<br>Chờ duyệt;<br>Thời gian bắt đầu > Thời gian hiện tại;<br>Thời gian hoạt động không trùng với phiên bản nào ở trạng thái Chờ lên lịch hoặc hiện hành;<br>Kết quả đầu ra:<br>Chuyển bộ quy tắc sang trạng thái "Đã lên lịch";<br>Ghi nhận người & ngày cập nhật;<br>Cập nhật ngày kết thúc của phiên bản đang hiện hành (nếu có) = ngày bắt đầu của phiên bản đang xét;<br>TH2: Từ chối:<br>Điều kiện:<br>Trạng thái của bộ quy tắc thuộc danh sách:<br>Chờ duyệt;<br>Kết quả đầu ra:<br>Chuyển bộ quy tắc sang trạng thái "Đã từ chối";<br>Ghi nhận người & ngày cập nhật.|

<img src="media/image12.png" id="image8">

##### Danh sách lượt nhập liệu

| # | # |
|---|---|
|Use Case|Danh sách lượt nhập liệu|
|Use Case ID||
|Description|Cho phép xem danh sách lượt nhập liệu|
|Actor|Primary Actor(s): Nhân viên khai giá; Quản lý giá<br>Secondary Actor(s):&nbsp;Admin hệ thống|
|Pre-Condition|User đăng nhập thành công vào web SCS;<br>Phần tử lương có hình thức tính là “Thủ công”;|
|Trigger|SCS → Quản lý quy tắc nghiệp vụ → Chọn 1 phần tử lương có hình thức là “Thủ công”|
|Post-Condition|Xem được danh sách các lượt nhập liệu tương ứng.|
|Priority|Medium|
|Business Rule|BR01. Kiểm tra tính hợp lệ của bộ lọc.<br>(BL1) Từ khóa: Chuỗi 0-255 ký tự, không chứa khoảng cách đầu cuối;<br>BR02. Lấy ra tất cả lượt nhập file t/m tất cả các điều kiện sau, điều kiện nào để trống thì coi như thỏa mãn:<br>Có tên chứa từ khóa được nhập vào tại (BL1) không phân biệt hoa thường, dấu;<br>BR03. Cột hiển thị, chọn 1 hoặc nhiều cột để hiển thị, bao gồm:<br>STT;<br>Tên file;<br>Số bản ghi;<br>Số bản ghi thành công;<br>Số bản ghi thất bại;<br>Thời gian cập nhật;<br>Người cập nhật;<br>Trạng thái: Soạn thảo / Chờ duyệt / Đã từ chối / Đã nhập;<br>Ghi chú;<br>Thao tác riêng:<br>Tải xuống;<br>Xóa: Chỉ hiện ở trạng thái Soạn thảo & Đã từ chối;<br>Đề xuất: Chỉ hiện ở trạng thái Soạn thảo.<br>BR04. Sắp xếp: Chọn 1 trong các lựa chọn:<br>Theo tên file(A→Z);<br>Theo thời gian cập nhật (mới → cũ).<br>BR05. Phân trang: 10 bản ghi/trang.|

<img src="media/image13.png" id="image9">

##### Nhập liệu

18.04.2026 Bổ sung file mẫu nhập cho đại lý

| # | # |
|---|---|
|Use Case|Nhập liệu|
|Use Case ID||
|Description|Cho phép người dùng nhập liệu cho các phần tử giá thủ công.|
|Actor|Primary Actor(s): Nhân viên khai giá; Quản lý giá<br>Secondary Actor(s):&nbsp;Admin hệ thống|
|Pre-Condition|User đăng nhập thành công vào web SCS;<br>Phần tử lương có hình thức tính là “Thủ công”;|
|Trigger|SCS → Quản lý quy tắc nghiệp vụ → Chọn 1 phần tử lương → Thao tác chung “Nhập file .xlsx”|
|Post-Condition|Dữ liệu được ghi nhận thành công vào CSDL.|
|Priority|Medium|
|Flow|1. Kiểm tra file nhập;<br>2. Duyệt từng bản ghi & tiến hành nhập liệu;<br>3. Ghi nhận kết quả lượt nhập file vào CSDL:<br>Ghi nhận lượt nhập dữ liệu (chưa ghi vào thù lao).|
|Business Rule|Cho phép tải file mẫu.|

<img src="media/image14.png" id="image10">

File mẫu đối với nhân viên

| # | # | # | # |
|---|---|---|---|
|Ngày<br>(YYYYMMDD)|Mã nhân viên|Mã bưu cục|Số tiền|
|||||
|||||

File mẫu đối với đại lý

| # | # | # |
|---|---|---|
|Ngày<br>(YYYYMMDD)|Mã đại lý|Số tiền|
||||
||||

##### Xóa lượt nhập liệu:

| # | # |
|---|---|
|Use Case|Xóa lượt nhập liệu|
|Use Case ID|UC2.2.3|
|Description|Cho phép xóa 1 lượt nhập liệu.|
|Actor|Primary Actor(s): Nhân viên khai giá; Quản lý giá<br>Secondary Actor(s):&nbsp;Admin hệ thống|
|Pre-Condition|User đăng nhập thành công vào web SCS.|
|Trigger|SCS → Quản lý nghiệp vụ → Chọn 1 phần tử lương có hình thức thủ công → Thao tác riêng “Xóa”|
|Post-Condition|Xóa thành công lượt nhập liệu.|
|Priority|Medium|
|Business Rule|Chỉ xóa ở trạng thái “Soạn thảo” & “Đã từ chối”.|

##### Đề xuất lượt nhập liệu:

| # | # |
|---|---|
|Use Case|Đề xuất lượt nhập liệu|
|Use Case ID||
|Description|Cho phép người dùng đề xuất 1 phiên bản.|
|Actor|Primary Actor(s): Quản lý giá, Nhân viên khai giá<br>Secondary Actor(s):&nbsp;Admin hệ thống|
|Pre-Condition|User đăng nhập thành công vào web SCS.|
|Trigger|SCS → Quản lý quy tắc nghiệp vụ → Danh sách bộ quy tắc → Thao tác riêng “Đề xuất”|
|Post-Condition|Đề xuất phiên bản thành công.|
|Priority|Medium|
|Business Rule|Điều kiện:<br>Trạng thái của lượt nhập liệu thuộc danh sách:<br>Soạn thảo;<br>Đã từ chối;<br>Số bản ghi hợp lệ > 0;<br>Kết quả đầu ra:<br>Chuyển lượt nhập liệu sang trạng thái "Chờ duyệt";<br>Ghi nhận người & ngày cập nhật.|

<img src="media/image15.png" id="image11">

##### Phê duyệt lượt nhập liệu:

| # | # |
|---|---|
|Use Case|Phê duyệt lượt nhập liệu|
|Use Case ID||
|Description|Cho phép người dùng phê duyệt 1 lượt nhập liệu.|
|Actor|Primary Actor(s): Quản lý giá<br>Secondary Actor(s):&nbsp;Admin hệ thống|
|Pre-Condition|User đăng nhập thành công vào web SCS.|
|Trigger|SCS → Quản lý quy tắc nghiệp vụ → Danh sách bộ quy tắc → Thao tác riêng “Phê duyệt”;|
|Post-Condition|Phê duyệt lượt nhập liệu thành công.|
|Priority|Medium|
|Business Rule|TH1: Đồng ý<br>Điều kiện:<br>Trạng thái của bộ quy tắc thuộc danh sách:<br>Chờ duyệt;<br>Số bản ghi hợp lệ > 0;<br>Kết quả đầu ra:<br>Chuyển bộ quy tắc sang trạng thái "Đã duyệt";<br>Ghi nhận người & ngày cập nhật;<br>Ghi nhận chi tiết thù lao trạng thái theo quy tắc dưới đây:<br>Hủy tất cả các bản ghi đã tồn tại trước đó bằng cách ghi nhận bản ghi âm, đây là các bản ghi thỏa mãn:<br>Phần tử lương = Phần tử cần tính;<br>Ngày khoán_Nhân viên_bưu cục = Ngày khoán_nhân viên_bưu cục được import;<br>Thêm mới bản ghi để ghi nhận kết quả mới;TH2: Từ chối:<br>Điều kiện:<br>Trạng thái của bộ quy tắc thuộc danh sách:<br>Chờ duyệt;<br>Kết quả đầu ra:<br>Chuyển bộ quy tắc sang trạng thái "Đã từ chối";<br>Ghi nhận người & ngày cập nhật;<br>Chuyển thù lao đã nhập|

<img src="media/image16.png" id="image12">

#### Quản lý dữ liệu

25.04.2026 – Bổ sung chức năng quản lý dữ liệu

##### Xem dữ liệu

| # | # |
|---|---|
|Use Case|Xem dữ liệu|
|Use Case ID||
|Description|Cho phép người dùng xem toàn bộ dữ liệu của 1 loại dữ liệu trong 1 kỳ.|
|Actor|Primary Actor(s): Quản lý dữ liệu<br>Secondary Actor(s):&nbsp;Admin hệ thống|
|Pre-Condition|User đăng nhập thành công vào web SCS;<br>User được phân quyền sử dụng chức năng Quản lý dữ liệu.|
|Trigger|SCS → Quản lý dữ liệu.|
|Post-Condition|Xem được dữ liệu đã nhập|
|Priority|Medium|
|Business Rule|BR01. Kiểm tra tính hợp lệ của bộ lọc.<br>(BL1) Tháng: Bắt buộc, chọn 1 tháng trong danh sách;<br>(BL2) Phân loại: Bắt buộc, chọn “Bưu cục” / “Nhân viên”;<br>(BL3) Dữ liệu: Bắt buộc, chọn trong danh sách:<br>(BL2) = Bưu cục:<br>Doanh thu kế hoạch;<br>(BL2) = Nhân viên:<br>Bậc và bước lương;<br>Tỷ lệ hoàn thành KPI cá nhân;<br>Số ngày nghỉ;<br>(BL4) Từ khóa: Chuỗi 0-255 ký tự, không chứa khoảng cách đầu cuối;<br>BR02. Quy tắc tìm kiếm:<br>Nếu (BL2) = Bưu cục, lấy ra tất cả các bưu cục thoả mãn, tiêu chí nào bỏ trống thì coi như thoả mãn:<br>Có dữ liệu (BL3) trong tháng (BL1);<br>Tên bưu cục chứa (BL4) hoặc mã bưu cục = (BL4), không phân biệt hoa thường, dấu;<br>Nếu (BL3) = Nhân viên, lấy ra tất cả các kết hợp bưu cục + nhân viên thoả mãn, tiêu chí nào bỏ trống thì coi như thoả mãn:<br>Có dữ liệu (BL3) trong tháng (BL1);<br>Tên nhân viên chứa (BL4) hoặc mã nhân viên = (BL4), không phân biệt hoa thường, dấu;<br>BR03. Cột hiển thị, chọn 1 hoặc nhiều cột để hiển thị, bao gồm:<br>| # | # |<br>|---|---|<br>|Loại dữ liệu (BL3)|Cột hiển thị|<br>|Doanh thu kế hoạch|Mã bưu cục;<br>Tên bưu cục;<br>Doanh thu kế hoạch trước thuế VAT;<br>Doanh thu kế hoạch sau thuế VAT|<br>|Bậc và bước lương|Mã bưu cục;<br>Mã nhân viên;<br>Tên nhân viên;<br>HRL;<br>Bước|<br>|Tỷ lệ hoàn thành KPI cá nhân|Mã bưu cục;<br>Mã nhân viên;<br>Tên nhân viên;<br>Tỷ lệ hoàn thành KPI cá nhân.|<br>|Số ngày nghỉ|Mã bưu cục;<br>Mã nhân viên;<br>Tên nhân viên;<br>Số ngày nghỉ.|<br>BR04. Sắp xếp: Chọn 1 trong các lựa chọn:<br>Theo mã bưu cục / tên nhân viên (A→Z);<br>BR05. Phân trang: 10 bản ghi/trang.<br>BR06. Cho phép xuất dữ liệu dưới dạng .xlsx, các cột như giao diện.|Loại dữ liệu (BL3)|Cột hiển thị|Doanh thu kế hoạch|Mã bưu cục;<br>Tên bưu cục;<br>Doanh thu kế hoạch trước thuế VAT;<br>Doanh thu kế hoạch sau thuế VAT|Bậc và bước lương|Mã bưu cục;<br>Mã nhân viên;<br>Tên nhân viên;<br>HRL;<br>Bước|Tỷ lệ hoàn thành KPI cá nhân|Mã bưu cục;<br>Mã nhân viên;<br>Tên nhân viên;<br>Tỷ lệ hoàn thành KPI cá nhân.|Số ngày nghỉ|Mã bưu cục;<br>Mã nhân viên;<br>Tên nhân viên;<br>Số ngày nghỉ.|
|Loại dữ liệu (BL3)|Cột hiển thị|
|Doanh thu kế hoạch|Mã bưu cục;<br>Tên bưu cục;<br>Doanh thu kế hoạch trước thuế VAT;<br>Doanh thu kế hoạch sau thuế VAT|
|Bậc và bước lương|Mã bưu cục;<br>Mã nhân viên;<br>Tên nhân viên;<br>HRL;<br>Bước|
|Tỷ lệ hoàn thành KPI cá nhân|Mã bưu cục;<br>Mã nhân viên;<br>Tên nhân viên;<br>Tỷ lệ hoàn thành KPI cá nhân.|
|Số ngày nghỉ|Mã bưu cục;<br>Mã nhân viên;<br>Tên nhân viên;<br>Số ngày nghỉ.|

Doanh thu kế hoạch:

<img src="media/image17.png" id="image13">

Bậc & bước lương:

<img src="media/image18.png" id="image14">

Tỷ lệ hoàn thành doanh thu cá nhân:

<img src="media/image19.png" id="image15">

Số ngày nghỉ:

<img src="media/image20.png" id="image16">

##### Xoá dữ liệu

| # | # |
|---|---|
|Use Case|Xoá dữ liệu|
|Use Case ID||
|Description|Cho phép người dùng xoá toàn bộ dữ liệu của kết hợp tháng + loại dữ liệu|
|Actor|Primary Actor(s): Quản lý dữ liệu<br>Secondary Actor(s):&nbsp;Admin hệ thống|
|Pre-Condition|User đăng nhập thành công vào web SCS;<br>Phần tử lương có hình thức tính là “Thủ công”;|
|Trigger|SCS → Quản lý dữ liệu → Chọn tháng & loại dữ liệu cần xoá  → Xoá dữ liệu.|
|Post-Condition|Dữ liệu được ghi nhận thành công vào CSDL.|
|Priority|Medium|
|Main Flow|1. Người dùng chọn “Xoá dữ liệu”;<br>2. Hệ thống kiểm tra người dùng đã chọn tháng & loại dữ liệu muốn xoá hay chưa;<br>3. (Yes) Đã chọn tháng & loại dữ liệu;<br>4. Hệ thống xác nhận yêu cầu xoá dữ liệu “Bạn có chắc chắn muốn xoá toàn bộ dữ liệu <Tên loại dữ liệu> khỏi kỳ <tháng>?”<br>5. (Yes) Người dùng xác nhận;<br>6. Hệ thống thực hiện xoá toàn bộ dữ liệu thuộc loại dữ liệu & tháng đã chọn.<br>Use Case hoàn thành.|
|Exception Flow|3. (No) Chưa chọn tháng hoặc loại dữ liệu;<br>7. Hệ thống báo lỗi tương ứng, yêu cầu người dùng chọn đủ các trường bắt buộc.<br>Use Case kết thúc.<br>5. (Yes) Người dùng huỷ.<br>Use Case kết thúc.|
|Business Rule||

##### Nhập dữ liệu

| # | # |
|---|---|
|Use Case|Nhập dữ liệu|
|Use Case ID||
|Description|Cho phép người dùng nhập dữ liệu của 1 loại dữ liệu vào 1 kỳ.|
|Actor|Primary Actor(s): Quản lý dữ liệu<br>Secondary Actor(s):&nbsp;Admin hệ thống|
|Pre-Condition|User đăng nhập thành công vào web SCS;<br>User được phân quyền vào chức năng Quản lý dữ liệu.|
|Trigger|SCS → Quản lý dữ liệu → Chọn tháng & loại dữ liệu cần xoá  → Nhập dữ liệu.|
|Post-Condition|Dữ liệu được ghi nhận thành công vào CSDL.|
|Priority|Medium|
|Main Flow|1. Người dùng chọn nút “Nhập dữ liệu” từ màn hình Quản lý dữ liệu;<br>2. Hệ thống hiển thị modal để người dùng tải file mẫu & tải lên file excel;<br>3. Người dùng chọn tệp Excel từ máy và nhấn nút "Xác nhận";<br>4. Hệ thống kiểm tra định dạng của tệp: <br>Định dạng hợp lệ: .xls hoặc .xlsx;<br>Kích cỡ tối đa: 10 Mb;<br>5. (Yes) – Tệp hợp lệ;<br>6. Hệ thống đọc dữ liệu từ file excel, kiểm tra tính hợp lệ và nhập từng dòng vào CSDL;<br>7. Hệ thống thông báo kết quả nhập liệu cho người dùng.<br>Use Case hoàn thành.|
|Exception Flow|5. Tệp không hợp lệ;<br>8. Hệ thống báo lỗi tương ứng.<br>Use Case kết thúc.|
|Business Rule|BR01. Quy tắc kiểm tra tính hợp lệ của từng bản ghi:<br>| # | # | # |<br>|---|---|---|<br>|Trường dữ liệu|Loại dữ liệu|Mô tả|<br>|Dữ liệu bưu cục|||<br>|Mã bưu cục|Chuỗi|Bắt buộc;<br>Chuỗi 0-50 ký tự, chỉ chứa chữ cái và số, tự động loại bỏ khoảng trắng đầu cuối;<br>Phải tồn tại trong danh mục bưu cục.|<br>|Doanh thu kế hoạch trước thuế (USD)|Số|Bắt buộc;<br>Là số dương, làm tròn tới 2 chữ số thập phân.|<br>|Doanh thu kế hoạch sau thuế (USD)|Số|Bắt buộc;<br>Là số dương, làm tròn lên tới 2 chữ số thập phân.|<br>|Dữ liệu nhân viên|||<br>|Mã bưu cục|Chuỗi|Bắt buộc;<br>Chuỗi 0-50 ký tự, chỉ chứa chữ cái và số, tự động loại bỏ khoảng trắng đầu cuối;<br>Phải tồn tại trong danh mục bưu cục.|<br>|Mã nhân viên|Chuỗi|Bắt buộc;<br>Chuỗi 0-50 ký tự, chỉ chứa chữ cái và số, tự động loại bỏ khoảng trắng đầu cuối;<br>Kết hợp mã nhân viên + Mã bưu cục phải tồn tại.|<br>|Số ngày nghỉ|Số|Bắt buộc;<br>Là số dương, làm tròn tới 2 chữ số thập phân.|<br>|HRL|Số|Bắt buộc;<br>Là số dương, làm tròn tới 2 chữ số thập phân.|<br>|Bước|Số|Bắt buộc;<br>Là số dương, làm tròn tới 2 chữ số thập phân.|<br>|Tỷ lệ hoàn thành KPI cá nhân|Số|Bắt buộc;<br>Làm tròn tới 2 chữ số thập phân.|<br>BR02. Quy tắc upsert dữ liệu:<br>Với loại dữ liệu bưu cục: Nếu chưa tồn tại tháng + bưu cục + dữ lieu đang xét thì insert, nếu đã tồn tại thì update;<br>Với loại dữ liệu nhân viên: Nếu chưa tồn tại tháng + bưu cục + nhân viên + dữ liệu đang xét thì insert, nếu đã tồn tại thì update.|Trường dữ liệu|Loại dữ liệu|Mô tả|Dữ liệu bưu cục|||Mã bưu cục|Chuỗi|Bắt buộc;<br>Chuỗi 0-50 ký tự, chỉ chứa chữ cái và số, tự động loại bỏ khoảng trắng đầu cuối;<br>Phải tồn tại trong danh mục bưu cục.|Doanh thu kế hoạch trước thuế (USD)|Số|Bắt buộc;<br>Là số dương, làm tròn tới 2 chữ số thập phân.|Doanh thu kế hoạch sau thuế (USD)|Số|Bắt buộc;<br>Là số dương, làm tròn lên tới 2 chữ số thập phân.|Dữ liệu nhân viên|||Mã bưu cục|Chuỗi|Bắt buộc;<br>Chuỗi 0-50 ký tự, chỉ chứa chữ cái và số, tự động loại bỏ khoảng trắng đầu cuối;<br>Phải tồn tại trong danh mục bưu cục.|Mã nhân viên|Chuỗi|Bắt buộc;<br>Chuỗi 0-50 ký tự, chỉ chứa chữ cái và số, tự động loại bỏ khoảng trắng đầu cuối;<br>Kết hợp mã nhân viên + Mã bưu cục phải tồn tại.|Số ngày nghỉ|Số|Bắt buộc;<br>Là số dương, làm tròn tới 2 chữ số thập phân.|HRL|Số|Bắt buộc;<br>Là số dương, làm tròn tới 2 chữ số thập phân.|Bước|Số|Bắt buộc;<br>Là số dương, làm tròn tới 2 chữ số thập phân.|Tỷ lệ hoàn thành KPI cá nhân|Số|Bắt buộc;<br>Làm tròn tới 2 chữ số thập phân.|
|Trường dữ liệu|Loại dữ liệu|Mô tả|
|Dữ liệu bưu cục|||
|Mã bưu cục|Chuỗi|Bắt buộc;<br>Chuỗi 0-50 ký tự, chỉ chứa chữ cái và số, tự động loại bỏ khoảng trắng đầu cuối;<br>Phải tồn tại trong danh mục bưu cục.|
|Doanh thu kế hoạch trước thuế (USD)|Số|Bắt buộc;<br>Là số dương, làm tròn tới 2 chữ số thập phân.|
|Doanh thu kế hoạch sau thuế (USD)|Số|Bắt buộc;<br>Là số dương, làm tròn lên tới 2 chữ số thập phân.|
|Dữ liệu nhân viên|||
|Mã bưu cục|Chuỗi|Bắt buộc;<br>Chuỗi 0-50 ký tự, chỉ chứa chữ cái và số, tự động loại bỏ khoảng trắng đầu cuối;<br>Phải tồn tại trong danh mục bưu cục.|
|Mã nhân viên|Chuỗi|Bắt buộc;<br>Chuỗi 0-50 ký tự, chỉ chứa chữ cái và số, tự động loại bỏ khoảng trắng đầu cuối;<br>Kết hợp mã nhân viên + Mã bưu cục phải tồn tại.|
|Số ngày nghỉ|Số|Bắt buộc;<br>Là số dương, làm tròn tới 2 chữ số thập phân.|
|HRL|Số|Bắt buộc;<br>Là số dương, làm tròn tới 2 chữ số thập phân.|
|Bước|Số|Bắt buộc;<br>Là số dương, làm tròn tới 2 chữ số thập phân.|
|Tỷ lệ hoàn thành KPI cá nhân|Số|Bắt buộc;<br>Làm tròn tới 2 chữ số thập phân.|

File mẫu nhập:

- Doanh thu kế hoạch:

| # | # | # |
|---|---|---|
|Mã bưu cục|Doanh thu kế hoạch trước thuế (USD)|Doanh thu kế hoạch sau thuế (USD)|
|TN2|500000|500000|

- HRL & Bước lương:

| # | # | # | # |
|---|---|---|---|
|Mã bưu cục|Mã nhân viên|HRL|Bước|
|TN2|123456|17|20|

- Số ngày nghỉ:

| # | # | # |
|---|---|---|
|Mã bưu cục|Mã nhân viên|Số ngày nghỉ (ngày)|
|TN2|123456|3|

- Tỷ lệ hoàn thành KPI cá nhân

| # | # | # |
|---|---|---|
|Mã bưu cục|Mã nhân viên|Tỷ lệ hoàn thành KPI cá nhân (%)|
|TN2|123456|90|

## Tiến trình tự động
##### Tự động kích hoạt & bất hoạt phiên bản

| # | # |
|---|---|
|Use Case|Tự động kích hoạt & bất hoạt phiên bản.|
|Use Case ID||
|Description|Tự động kích hoạt & bất hoạt phiên bản.|
|Actor||
|Pre-Condition|User đăng nhập thành công vào web SCS.|
|Trigger|1h mỗi lần, chạy job vào các khung giờ HH:01|
|Post-Condition|Phiên bản đã lên lịch được kích hoạt;<br>Phiên bản sắp kết thúc được bất hoạt;|
|Priority|High|
|Business Rule|1. Kích hoạt:<br>Lấy ra các phiên bản thỏa mãn:<br>Trạng thái = “Đã lên lịch”;<br>Thời gian bắt đầu < Thời gian chạy job;<br>Thực hiện:<br>Cập nhật trạng thái = “Kích hoạt”;<br>Ghi nhận ngày cập nhật;<br>2. Bất hoạt:<br>Lấy ra các phiên bản thỏa mãn:<br>Trạng thái = “Hiện hành”;<br>Thời gian kết thúc < Thời gian chạy job;<br>Thực hiện:<br>Cập nhật trạng thái = “Đã dừng”;<br>Ghi nhận ngày cập nhật;|

## Tính lương
### Tính lương theo sự kiện

06.04.2026 Bổ sung luồng tính lương từ sự kiện hoàn thành chuyến xe;

18.04.2026 Tách phần tử hoa hồng nhận đại lý;

25.04.2026 Bổ sung các luồng tính lương KHM, lương cứng, hoàn thành KPI, khai thác.

| # | # |
|---|---|
|Use Case|Tính lương theo sự kiện|
|Use Case ID||
|Description|Tính lương khi giao thành công|
|Actor|Hệ thống lương khoán|
|Pre-Condition|-|
|Trigger|Phát sinh sự kiện, bao gồm:<br>Nhận được bản tin đơn hàng giao/nhận/kết nối thành công tại topic Kafka tương ứng;<br>Tới thời điểm chốt ngày/tháng tự động sinh các sự kiện chốt thù lao & doanh thu;|
|Post-Condition|Tính ra & ghi nhận các khoản thù lao tương ứng cho nhân viên & đại lý.|
|Priority|High|
|Flow|1. Sự kiện phát sinh;<br>2. Tiền xử lý:<br>Kiểm tra toàn vẹn dữ liệu;<br>Nạp tham số;<br>Nạp file quy tắc hiện hành tương ứng;<br>3. Truyền tham số qua file quy tắc;<br>4. Hậu xử lý & ghi nhận dữ liệu.|
|Business Rule|Bản ghi lỗi ghi lại dạng dead letter phục vụ giám sát;<br>Tham số cần sử dụng tại từng luồng tham chiếu tới PL01.|

Chi tiết cách xử lý từng sự kiện.

| # | # |
|---|---|
|Sự kiện|Mô tả|
|1. Nhận bản tin đơn hàng được giao thành công|1. Nhận bản tin từ topic phát thành công;<br>2. Kiểm tra toàn vẹn dữ liệu & xử lý tham số;<br>3. Tính lương:<br>Truyền tham số qua rule set của các phần tử lương có sự kiện tính toán là “Giao hàng”, bao gồm:<br>EmpBaseDeliveryFee;<br>EmpWeightDeliveryFee;<br>AgtDeliveryFee.<br>4. Hậu xử lý:<br>TH1:<br>Nếu: Sự kiện đã được ghi nhận thù lao trước đó:<br>Phần tử lương có sự kiện tính toán = Giao hàng;<br>Mã vận đơn = Mã vận đơn của lượt giao cần tính;<br>Thì:<br>Hủy tất cả các bản ghi thù lao đã tồn tại trước đó bằng cách ghi nhận bản ghi âm;<br>Ghi nhận bản ghi thù lao để ghi nhận kết quả mới;<br>Ghi nhận sự kiện đã tính;<br>TH2:<br>Nếu: Sự kiện chưa được ghi nhận thù lao trước đó:<br>Thì: <br>Ghi nhận bản ghi thù lao để ghi nhận kết quả mới;<br>Ghi nhận sự kiện đã tính;|
|2. Nhận bản tin đơn hàng được nhận thành công|1. Nhận bản tin từ topic nhận thành công;<br>2. Kiểm tra toàn vẹn dữ liệu;<br>3. Tính lương:<br>Truyền tham số qua rule set của các phần tử lương có kiện tính toán là “Nhận hàng”, bao gồm:<br>EmpBasePickupFee;<br>EmpWeightPickupFee;<br>AgtPickupFee;<br>4. Hậu xử lý:<br>TH1:<br>Nếu: Sự kiện đã được ghi nhận thù lao trước đó:<br>Phần tử lương có sự kiện tính toán = Nhận hàng;<br>Mã vận đơn = Mã vận đơn của lượt nhận cần tính;<br>Thì:<br>Hủy tất cả các bản ghi thù lao đã tồn tại trước đó bằng cách ghi nhận bản ghi âm;<br>Ghi nhận bản ghi thù lao để ghi nhận kết quả mới;<br>Ghi nhận sự kiện đã tính;<br>TH2:<br>Nếu: Sự kiện chưa được ghi nhận thù lao trước đó:<br>Thì: <br>Ghi nhận bản ghi thù lao để ghi nhận kết quả mới;<br>Ghi nhận sự kiện đã tính;|
|3. Nhận bản tin chuyến xe hoàn thành|1. Nhận bản tin từ topic hoàn thành chuyến xe;<br>2. Kiểm tra toàn vẹn dữ liệu;<br>3. Tính lương:<br>Truyền tham số qua rule set của các phần tử lương có kiện tính toán là “Hoàn thành chuyến xe”, bao gồm:<br>EmpTransportFee;<br>4. Hậu xử lý:<br>TH1:<br>Nếu: Sự kiện đã được ghi nhận thù lao trước đó:<br>Phần tử lương có sự kiện tính toán = Hoàn thành chuyến xe;<br>Mã chuyến xe = Mã chuyến xe đang xét;<br>Thì:<br>Hủy tất cả các bản ghi thù lao đã tồn tại trước đó bằng cách ghi nhận bản ghi âm;<br>Ghi nhận bản ghi thù lao để ghi nhận kết quả mới;<br>Ghi nhận sự kiện đã tính;<br>TH2:<br>Nếu: Sự kiện chưa được ghi nhận thù lao trước đó:<br>Thì: <br>Ghi nhận bản ghi thù lao để ghi nhận kết quả mới;<br>Ghi nhận sự kiện đã tính;|
|4. Chốt doanh thu nhận hàng trong tháng|1. Tới 1:00 AM ngày 1 hằng tháng;<br>2. Nạp dữ liệu;<br>Lấy ra toàn bộ sự kiện nhận hàng thỏa mãn:<br>Loại bưu cục nhận hàng = Đại lý (AGENT);<br>Thời gian nhận hàng trong tháng n;<br>Nạp tham số cho mỗi bản ghi;<br>3. Tính lương:<br>Truyền tham số qua rule set của các phần tử lương có sự kiện tính toán là “Chốt doanh thu nhận hàng trong tháng”, bao gồm:<br>AgtPickupFeeAdjustment<br>4. Hậu xử lý:<br>TH1:<br>Nếu: Sự kiện đã được ghi nhận thù lao trước đó:<br>Phần tử lương có sự kiện tính toán = Chốt doanh thu nhận hàng trong tháng;<br>Mã vận đơn = Mã vận đơn của sự kiện đang xét;<br>Thì:<br>Hủy tất cả các bản ghi thù lao đã tồn tại trước đó bằng cách ghi nhận bản ghi âm;<br>Ghi nhận bản ghi thù lao để ghi nhận kết quả mới;<br>Ghi nhận sự kiện đã tính;<br>TH2:<br>Nếu: Sự kiện chưa được ghi nhận thù lao trước đó:<br>Thì: <br>Ghi nhận bản ghi thù lao để ghi nhận kết quả mới;<br>Ghi nhận sự kiện đã tính;|
|5. Nhận bản tin khách hàng mới|1. Nhận bản tin từ topic khách hàng mới;<br>2. Kiểm tra toàn vẹn dữ liệu & xử lý tham số;<br>3. Tính lương:<br>Truyền tham số qua rule set của các phần tử lương có sự kiện tính toán là “Khách hàng mới” bao gồm:<br>EmpCustomerDevelopmentFee.<br>4. Hậu xử lý:<br>TH1:<br>Nếu: Sự kiện đã được ghi nhận thù lao trước đó:<br>Phần tử lương có sự kiện tính toán = Khách hàng mới;<br>ID Khách hàng = ID Khách hàng đang xét;<br>Tháng khoán = Tháng đang xét.<br>Thì:<br>Hủy tất cả các bản ghi thù lao đã tồn tại trước đó bằng cách ghi nhận bản ghi âm;<br>Ghi nhận bản ghi thù lao để ghi nhận kết quả mới;<br>Ghi nhận sự kiện đã tính;<br>TH2:<br>Nếu: Sự kiện chưa được ghi nhận thù lao trước đó:<br>Thì: <br>Ghi nhận bản ghi thù lao để ghi nhận kết quả mới;<br>Ghi nhận sự kiện đã tính;|
|Tính lương cứng|1. Lấy ra toàn bộ các kết hợp nhân viên + bưu cục;<br>2. Tổng hợp tham số;<br>3. Tính lương:<br>Truyền tham số qua rule set của các phần tử lương có sự kiện tính toán là “Lương cứng” bao gồm:<br>EmpBaseFee.<br>4. Hậu xử lý:<br>TH1:<br>Nếu: Sự kiện đã được ghi nhận thù lao trước đó:<br>Phần tử lương có sự kiện tính toán = Lương cứng;<br>Nhân viên = Nhân viên đang xét;<br>Bưu cục = Bưu cục đang xét;<br>Tháng khoán = Tháng đang xét.<br>Thì:<br>Hủy tất cả các bản ghi thù lao đã tồn tại trước đó bằng cách ghi nhận bản ghi âm;<br>Ghi nhận bản ghi thù lao để ghi nhận kết quả mới;<br>Ghi nhận sự kiện đã tính;<br>TH2:<br>Nếu: Sự kiện chưa được ghi nhận thù lao trước đó:<br>Thì: <br>Ghi nhận bản ghi thù lao để ghi nhận kết quả mới;<br>Ghi nhận sự kiện đã tính;|
|Thù lao hoàn thành KPI|1. Lấy ra toàn bộ các kết hợp nhân viên + bưu cục;<br>2. Tổng hợp tham số;<br>3. Tính lương:<br>Truyền tham số qua rule set của các phần tử lương có sự kiện tính toán là “Hoàn thành KPI” bao gồm:<br>EmpKpiFee.<br>4. Hậu xử lý:<br>TH1:<br>Nếu: Sự kiện đã được ghi nhận thù lao trước đó:<br>Phần tử lương có sự kiện tính toán = Hoàn thành KPI;<br>Nhân viên = Nhân viên đang xét;<br>Bưu cục = Bưu cục đang xét;<br>Tháng khoán = Tháng đang xét.<br>Thì:<br>Hủy tất cả các bản ghi thù lao đã tồn tại trước đó bằng cách ghi nhận bản ghi âm;<br>Ghi nhận bản ghi thù lao để ghi nhận kết quả mới;<br>Ghi nhận sự kiện đã tính;<br>TH2:<br>Nếu: Sự kiện chưa được ghi nhận thù lao trước đó:<br>Thì: <br>Ghi nhận bản ghi thù lao để ghi nhận kết quả mới;<br>Ghi nhận sự kiện đã tính;|
|Khai thác|1. Lấy ra toàn bộ các kết hợp nhân viên + bưu cục;<br>2. Tổng hợp tham số;<br>3. Tính lương:<br>Truyền tham số qua rule set của các phần tử lương có sự kiện tính toán là “Khai thác” bao gồm:<br>EmpHandlingFee.<br>4. Hậu xử lý:<br>TH1:<br>Nếu: Sự kiện đã được ghi nhận thù lao trước đó:<br>Phần tử lương có sự kiện tính toán = Khai thác;<br>Nhân viên = Nhân viên đang xét;<br>Bưu cục = Bưu cục đang xét;<br>Tháng khoán = Tháng đang xét.<br>Thì:<br>Hủy tất cả các bản ghi thù lao đã tồn tại trước đó bằng cách ghi nhận bản ghi âm;<br>Ghi nhận bản ghi thù lao để ghi nhận kết quả mới;<br>Ghi nhận sự kiện đã tính;<br>TH2:<br>Nếu: Sự kiện chưa được ghi nhận thù lao trước đó:<br>Thì: <br>Ghi nhận bản ghi thù lao để ghi nhận kết quả mới;<br>Ghi nhận sự kiện đã tính;|

## Báo cáo
### Luồng chạy ngầm
#### Tính tỷ lệ hoàn thành doanh thu 

25.04.2026 Bổ sung luồng tính báo cáo tỷ lệ hoàn thành doanh thu

| # | # |
|---|---|
|Use Case|Tính tỷ lệ hoàn thành doanh thu|
|Use Case ID||
|Description|Tính tỷ lệ hoàn thành doanh thu.|
|Actor|Người dùng SCS|
|Pre-Condition|User đăng nhập thành công vào web SCS.|
|Trigger|XX:XX ngày 3 tháng n+1 tính tỷ lệ hoàn thành doanh thu tháng n.|
|Post-Condition|Tỷ lệ hoàn thành doanh thu bưu cục, tỉnh, vùng được tính vào ghi nhận vào CSDL.|
|Priority|High|
|Flow|1. Kiểm tra đã có kỳ hay chưa;<br>2. No – Chưa tạo kỳ;<br>3. Tạo kỳ;<br>4. Tính tỷ lệ hoàn thành doanh thu bưu cục;<br>5. Lưu tỷ lệ hoàn thành doanh thu bưu cục vào CSDL;<br>6. Tính tỷ lệ hoàn thành doanh thu tỉnh;<br>7. Lưu tỷ lệ hoàn thành daonh thu tỉnh vào CSDL;<br>8. Tính tỷ lệ hoàn thành doanh thu vùng;<br>9. Lưu tỷ lệ hoàn thành doanh thu vùng vào CSDL.<br>10. Tính tỷ lệ hoàn thành doanh thu tổng;<br>11. Lưu tỷ lệ hoàn thành doanh thu tổng vào CSDL.<br>Use Case hoàn thành.|
|Business Rule||

Dịch vụ;

Huỷ đơn;

| # | # | # | # | # |
|---|---|---|---|---|
|Loại|Doanh thu thực hiện trước thuế (USD)|Doanh thu sau thuế|Doanh thu kế hoạch (USD)|TLHT doanh thu (%)|
|Bưu cục|Tổng cước dịch vụ chính (không bao thuế VAT) của các đơn hàng thỏa mãn:<br>Thời gian nhập doanh thu thuộc tháng n;<br>Bưu cục nhập doanh thu = Bưu cục đang xét.<br>* Mỗi mã vận đơn chỉ tính 1 lần.||Doanh thu kế hoạch được nhập liệu cho bưu cục đang xét.|Doanh thu thực hiện / Doanh thu kế hoạch * 100<br>Làm tròn tới số thập phân thứ 2.|
|Tỉnh|Tổng doanh thu thực hiện của các bưu cục thuộc tỉnh đang xét.||Tổng doanh thu kế hoạch của các bưu cục thuộc tỉnh đang xét.||
|Vùng|Tổng doanh thu thực hiện của các tỉnh thuộc vùng đang xét.||Tổng doanh thu kế hoạch của các tỉnh thuộc vùng đang xét.||

| # | # | # |
|---|---|---|
|Mã vùng|Tên vùng|Mã tỉnh|
|ZONE01|Vùng 1|KAN|
|ZONE01|Vùng 1|PNP|
|ZONE01|Vùng 1|PRE|
|ZONE01|Vùng 1|SVA|
|ZONE02|Vùng 2|KAM|
|ZONE02|Vùng 2|KOH|
|ZONE02|Vùng 2|SIH|
|ZONE02|Vùng 2|SPE|
|ZONE02|Vùng 2|TAK|
|ZONE03|Vùng 3|BAN|
|ZONE03|Vùng 3|BAT|
|ZONE03|Vùng 3|CHH|
|ZONE03|Vùng 3|PAI|
|ZONE03|Vùng 3|PUR|
|ZONE04|Vùng 4|ODD|
|ZONE04|Vùng 4|PRH|
|ZONE04|Vùng 4|SIE|
|ZONE04|Vùng 4|THO|
|ZONE05|Vùng 5|CHA|
|ZONE05|Vùng 5|KRA|
|ZONE05|Vùng 5|MON|
|ZONE05|Vùng 5|ROT|
|ZONE05|Vùng 5|STU|
|ZONE05|Vùng 5|TBK|

### Chức năng web SCS
#### Báo cáo SCS
#### Báo cáo thù lao nhân viên

18.04.2026 Điều chỉnh:

LV1:

Lọc theo đối tượng & chức danh;

Điều chỉnh số cột hiển thị;

LV2: Bổ sung mới;

LV3:

Điều chỉnh lọc phân loại;

Bổ sung màn hiển thị chi tiết chuyến xe.

25.04.2026 Bổ sung các màn chi tiết hiển thị lương khách hàng mới, lương cứng, lương hoàn thành KPI, lương khai thác

| # | # |
|---|---|
|Use Case|Báo cáo tổng hợp thù lao nhân viên|
|Use Case ID||
|Description|Báo cáo tổng hợp thù lao nhân viên.|
|Actor|Người dùng SCS|
|Pre-Condition|User đăng nhập thành công vào web SCS.|
|Trigger|SCS → Báo cáo → Báo cáo tổng hợp thù lao.|
|Post-Condition|Người dùng xem được báo cáo tổng hợp thù lao nhân viên.|
|Priority|High|
|Flow|LV1 → LV2 → LV3|
|Business Rule|Cho phép xuất báo cáo dưới dạng file .xlsx|

LV1:

<img src="media/image21.png" id="image17">

| # | # |
|---|---|
|Đầu vào|(BL1) Từ khóa: Chuỗi 0-255 ký tự, không chứa khoảng cách đầu cuối;<br>(BL2) Thời gian: Bắt buộc, chọn ngày – ngày, tối đa 31 ngày;<br>(BL3) Chi nhánh: Chọn 1 chi nhánh trong danh mục;<br>(BL4) Bưu cục: Chọn 1 bưu cục trong danh mục;<br>(BL5) Đối tượng: Chọn 1 đối tượng trong danh mục;<br>(BL6) Chức danh: Chọn 1 chức danh trong danh mục;<br>(SX1) Chọn trong danh mục bao gồm:<br>Theo tên nhân viên (A→Z);|
|Đầu ra|Lấy ra tất cả kết hợp bưu cục _ nhân viên t/m tất cả các điều kiện sau, điều kiện nào để trống thì coi như thỏa mãn:<br>Có tên chứa (BL1) không phân biệt hoa thường, dấu HOẶC SĐT chứa (BL1) HOẶC mã nhân viên bằng (BL1);<br>Phát sinh thù lao trong khoảng (BL2);<br>Chi nhánh trực thuộc = (BL3);<br>Bưu cục trực thuộc = (BL4);<br>Mỗi bản ghi lấy ra:<br>STT;<br>Mã chi nhánh;<br>Mã bưu cục;<br>Họ và tên;<br>Mã nhân viên;<br>Tên chức danh;<br>Tên đối tượng;<br>Sản lượng:<br>Giao hàng: Số mã vận đơn được bưu cục_nhân viên giao trong khoảng (BL2);<br>Nhận hàng: Số mã vận đơn dược bưu cục_nhân viên nhận trong khoảng (BL2);<br>Chuyến xe: Số mã chuyến xe được bưu cục_nhân viên hoàn thành trong khoảng (BL2);<br>Chi tiết thù lao theo cấu phần:<br>Bao gồm:<br>Lương cứng;<br>Lương khoán:<br>Hoàn thành KPI;<br>Giao hàng;<br>Nhận hàng;<br>Khai thác;<br>Kết nối;<br>Khách hàng mới;<br>Phụ cấp;<br>Thưởng phạt;<br>Khác (Bao gồm tất cả các cấu phần không thuộc danh sách kể trên);<br>Tổng = Lương cứng + Lương khoán + Khách hàng mới + Phụ cấp + Thưởng phạt + Khác;<br>Mỗi cấu phần lấy ra tổng tiền = tổng giá trị các giao dịch thỏa mãn:<br>Phần tử lương thuộc cấu phần lương tại cột đang xét (*);<br>Của bưu cục_nhân viên tại dòng đang xét;<br>Ngày khoán thuộc khoảng (BL2).|

LV2:

<img src="media/image22.png" id="image18">

| # | # |
|---|---|
|Đầu vào|(BL1) Nhân viên: Bắt buộc, tự động lấy nhân viên được chọn từ LV1;<br>(BL2) Thời gian: Bắt buộc, chọn ngày – ngày, tối đa 31 ngày, mặc định là thời gian đã chọn ở LV1;|
|Đầu ra|Thông tin sản lượng:<br>Giao hàng: Số mã vận đơn được bưu cục_nhân viên (BL1) giao trong khoảng (BL2);<br>Nhận hàng: Số mã vận đơn dược bưu cục_nhân viên (BL1) nhận trong khoảng (BL2);<br>Chuyến xe: Số mã chuyến xe được bưu cục_nhân viên (BL1) hoàn thành trong khoảng (BL2);<br> Thông tin lương:<br>Chi tiết cấu phần lương:<br>Bao gồm:<br>Lương cứng;<br>Lương khoán:<br>Thù lao hoàn thành KPI;<br>Thù lao giao;<br>Thù lao nhận;<br>Thù lao khai thác;<br>Thù lao kết nối;<br>Khách hàng mới;<br>Phụ cấp;<br>Thưởng phạt;<br>Khác (Các cấu phần không thuộc danh sách kể trên);<br>Mỗi cấu phần lấy ra:<br>Chi tiết các phần tử lương trong cấu phần đó:<br>Bao gồm các phần tử lương có ít nhất 01 giao dịch thỏa mãn:<br>Bưu cục_nhân viên hưởng = (BL1);<br>Ngày khoán thuộc (BL2);<br>Thuộc cấu phần đang xét;<br>Mỗi phần tử lấy ra:<br>Mã phần tử;<br>Tên phần tử;<br>Số giao dịch thỏa mãn:<br>Bưu cục_nhân viên hưởng là (BL1);<br>Thời gian phát sinh thuộc (BL2);<br>Phần tử lương = Phần tử lương đang xét;<br>Thành tiền: Tổng giá trị của các giao dịch kể trên;<br>Phân biệt hình thức tính toán tự động / thủ công;<br>Tổng thành tiền của các phần tử.|

LV3:

Với phần tử lương thủ công:

<img src="media/image23.png" id="image19">

Với phần tử lương tự động:

Với phần tử tính từ sự kiện = ”Giao hàng” / ”Nhận hàng”:

<img src="media/image24.png" id="image20">

Với phần tử tính từ sự kiện = ”Hoàn thành chuyến xe”:

<img src="media/image25.png" id="image21">

Với phần tử tính từ sự kiện = ”Khách hàng mới”:

<img src="media/image26.png" id="image22">

Với sự kiện: ”Lương cứng”

<img src="media/image27.png" id="image23">

Với sự kiện ”Khai thác”;

<img src="media/image28.png" id="image24">

Với sự kiện ”Chốt KPI”

<img src="media/image29.png" id="image25">

| # | # |
|---|---|
|Đầu vào|(BL1) Nhân viên: Bắt buộc, tự động lấy nhân viên được chọn;<br>(BL2) Bưu cục: Tự động lấy bưu cục được chọn;<br>(BL3) Thời gian: Bắt buộc, chọn ngày – ngày, tối đa 31 ngày;<br>(BL4) Phân loại: Bắt buộc, chọn 1 trong danh mục, mặc định chọn phân loại muốn xem chi tiết, cho phép chọn trong danh mục gồm:<br>Lương cứng;<br>Lương khoán:<br>Hoàn thành KPI;<br>Giao;<br>Nhận;<br>Khai thác;<br>Kết nối;<br>Khách hàng mới;<br>Phụ cấp;<br>Thưởng phạt;<br>Khác (Bao gồm các phần tử không thuộc danh sách kể trên);<br>(BL5) Phần tử lương: Bắt buộc, chọn 1 trong danh mục phần tử lương thuộc phân loại đã chọn ở (BL3);<br>(SX1) Chọn trong danh sách bao gồm:<br>Theo ngày khoán (Từ mới nhất tới cũ nhất);|
|Đầu ra|Lấy ra tất cả bản ghi thù lao thỏa mãn:<br>Nhân viên hưởng lương = (BL1);<br>Bưu cục hưởng lương = (BL2);<br>Ngày khoán thuộc (BL3);<br>Phần tử lương = (BL5);<br>Mỗi dòng lấy ra các thông tin sau:<br>Phần tử tự động:<br>STT;<br>Ngày khoán;<br>Tên loại sự kiện;<br>Thông tin chi tiết sự kiện (Tham chiếu phục lục);<br>Thời gian cập nhật giao dịch;<br>Thành tiền (USD);<br>Phần tử thủ công:<br>STT;<br>Ngày khoán;<br>Tên file nhập;<br>Người duyệt;<br>Thời gian duyệt;<br>Thời gian cập nhật giao dịch;<br>Thành tiền (USD).|

#### Báo cáo hoa hồng đại lý

Điều chỉnh:

LV1: Điều chỉnh số cột hiển thị;

LV2: Bổ sung mới;

LV3:

Điều chỉnh lọc phân loại;

Bổ sung màn hiển thị chi tiết khi sự kiện = Hoàn thành chuyến xe & Chốt doanh thu cuối tháng;

| # | # |
|---|---|
|Use Case|Báo cáo hoa hồng đại lý|
|Use Case ID||
|Description|Báo cáo hoa hồng đại lý.|
|Actor|Người dùng SCS|
|Pre-Condition|User đăng nhập thành công vào web SCS.|
|Trigger|SCS → Báo cáo → Báo cáo hoa hồng đại lý.|
|Post-Condition|Người dùng xem được báo cáo hoa hồng đại lý.|
|Priority|High|
|Flow||
|Business Rule|Cho phép xuất báo cáo dưới dạng file .xlsx|

LV1:

<img src="media/image30.png" id="image26">

| # | # |
|---|---|
|Đầu vào|(BL1) Từ khóa: Chuỗi 0-255 ký tự, không chứa khoảng cách đầu cuối;<br>(BL2) Thời gian: Chọn ngày – ngày, tối đa 31 ngày;<br>(BL3) Chi nhánh: Chọn 1 chi nhánh trong danh mục;<br>(SX1) Chọn trong danh mục bao gồm:<br>Theo mã bưu cục (A→Z);|
|Đầu ra|Lấy ra tất cả kết hợp bưu cục t/m tất cả các điều kiện sau, điều kiện nào để trống thì coi như thỏa mãn:<br>Thuộc loại đại lý;<br>Có tên chứa (BL1) không phân biệt hoa thường, dấu (BL1) HOẶC mã bằng bằng (BL1);<br>Phát sinh thù lao trong khoảng (BL2);<br>Chi nhánh trực thuộc = (BL3);<br>Mỗi bản ghi lấy ra:<br>STT;<br>Mã chi nhánh;<br>Tên bưu cục (đại lý);<br>Mã bưu cục (đại lý);<br>Sản lượng:<br>Giao hàng: Số mã vận đơn được bưu cục giao trong khoảng (BL2);<br>Nhận hàng: Số mã vận đơn dược bưu cục nhận trong khoảng (BL2);<br>Chi tiết thù lao theo cấu phần:<br>Bao gồm:<br>Hoa hồng giao;<br>Hoa hồng nhận;<br>Khác (bao gồm tất cả các cấu phần không thuộc danh sách kể trên);<br>Tổng = Hoa hồng giao + Hoa hồng nhận + Khác;<br>Mỗi cấu phần lấy ra tổng tiền = tổng các giao dịch thỏa mãn:<br>Phần tử lương thuộc cấu phần lương tại cột đang xét (*);<br>Của bưu cục_nhân viên tại dòng đang xét;<br>Ngày khoán thuộc khoảng (BL2).|

LV2:

<img src="media/image31.png" id="image27">

| # | # |
|---|---|
|Đầu vào|(BL1) Đại lý: Bắt buộc, tự động lấy đại lý được chọn từ LV1;<br>(BL2) Thời gian: Bắt buộc, chọn ngày – ngày, tối đa 31 ngày, mặc định là thời gian đã chọn ở LV1;|
|Đầu ra|Thông tin sản lượng:<br>Giao hàng: Số mã vận đơn được đại lý (BL1) giao trong khoảng (BL2);<br>Nhận hàng: Số mã vận đơn dược đại lý (BL1) nhận trong khoảng (BL2);<br> Thông tin lương:<br>Chi tiết cấu phần lương:<br>Bao gồm:<br>Hoa hồng giao;<br>Hoa hồng nhận;<br>Khác (Các cấu phần không thuộc danh sách kể trên);<br>Mỗi cấu phần lấy ra:<br>Chi tiết các phần tử lương trong cấu phần đó:<br>Bao gồm các phần tử lương có ít nhất 01 giao dịch thỏa mãn:<br>Đại lý hưởng = (BL1);<br>Ngày khoán thuộc (BL2);<br>Thuộc cấu phần đang xét;<br>Mỗi phần tử lấy ra:<br>Mã phần tử;<br>Tên phần tử;<br>Số giao dịch thỏa mãn:<br>Bưu cục hưởng là (BL1);<br>Thời gian phát sinh thuộc (BL2);<br>Phần tử lương = Phần tử lương đang xét;<br>Thành tiền: Tổng giá trị của các giao dịch kể trên;<br>Phân biệt hình thức tính toán tự động / thủ công;<br>Tổng thành tiền của các phần tử.|

LV3:

Với phần tử thủ công (hiện đại lý chưa có phần tử nào như vậy nhưng phát triển cho tổng quát):

<img src="media/image32.png" id="image28">

Với phần tử tự động:

Phần tử tính từ sự kiện giao hàng / nhận hàng (tương tự như nhân viên):

<img src="media/image33.png" id="image29">

Phần tử tính từ sự kiện hoàn thành chuyến xe (hiện đại lý chưa có phần tử nào như vậy nhưng phát triển cho tổng quát):

<img src="media/image34.png" id="image30">

Phần tử tính từ sự kiện chốt thù lao nhận tháng (tương tự giao/ nhận hàng nhưng thêm cột “Tổng doanh thu nhận tháng (USD)”:

<img src="media/image35.png" id="image31">

| # | # |
|---|---|
|Đầu vào|(BL1) Bưu cục: Bắt buộc, tự động lấy bưu cục được chọn ở LV2;<br>(BL2) Thời gian: Bắt buộc, chọn ngày – ngày, tối đa 31 ngày;<br>(BL3) Phân loại: Bắt buộc, chọn 1 trong danh mục, mặc định chọn phân loại muốn xem chi tiết, cho phép chọn trong danh mục gồm:<br>Hoa hồng giao;<br>Hoa hồng nhận;<br>Khác (Các phần tử không thuộc danh sách kể trên);<br>(BL4) Phần tử lương: Bắt buộc, chọn 1 trong danh mục phần tử lương thuộc phân loại đã chọn ở (BL3);<br>(SX1) Chọn trong danh sách bao gồm:<br>Theo ngày khoán (Từ mới nhất tới cũ nhất);|
|Đầu ra|Lấy ra tất cả bản ghi thù lao thỏa mãn:<br>Bưu cục hưởng lương = (BL1);<br>Ngày khoán thuộc (BL2);<br>Phần tử lương = (BL4);<br>Mỗi dòng lấy ra các thông tin sau:<br>Phần tử tự động:<br>STT;<br>Ngày khoán;<br>Tên loại sự kiện;<br>Thông tin chi tiết sự kiện (*);<br>Thời gian cập nhật giao dịch;<br>Thành tiền (USD);<br>Phần tử thủ công:<br>STT;<br>Ngày khoán;<br>Tên file nhập;<br>Người duyệt;<br>Thời gian duyệt;<br>Thời gian cập nhật giao dịch;<br>Thành tiền (USD).|

#### Báo cáo tỷ lệ hoàn thành doanh thu 

25.04.2026 Bổ sung báo cáo tỷ lệ hoàn thành doanh thu

| # | # |
|---|---|
|Use Case|Báo cáo tỷ lệ hoàn thành doanh thu|
|Use Case ID||
|Description|Chức năng cho phép người dùng tra cứu tỷ lệ hoàn thành doanh thu của bưu cục, tỉnh, vùng.|
|Actor||
|Pre-Condition|User đăng nhập thành công vào web SCS.|
|Trigger|Người dùng muốn tra cứu báo cáo tỷ lệ hoàn thành doanh thu.|
|Post-Condition|Phiên bản đã lên lịch được kích hoạt;<br>Phiên bản sắp kết thúc được bất hoạt;|
|Priority|High|
|Business Rule|Cho phép trích xuất báo cáo dưới dạng file .xlsx|

- Tra cứu theo vùng:

<img src="media/image36.png" id="image32">

| # | # |
|---|---|
|Đầu vào|(BL1) Từ khóa: Chuỗi 0-255 ký tự, không chứa khoảng cách đầu cuối;<br>(BL2) Kỳ báo cáo: Bắt buộc, chọn 01 kỳ báo cáo trong danh sách;<br>(SX1) Chọn trong danh sách bao gồm:<br>Theo mã vùng (A→Z);|
|Đầu ra|Lấy ra tất cả các vùng thỏa mãn, tiêu chí nào để trống thì coi như thỏa mãn:<br>Có tên chứa (BL1) hoặc mã = (BL1) không phân biệt hoa thường, dấu;<br>Được tính tỷ lệ hoàn thành doanh thu trong kỳ báo cáo (BL2);<br>Mỗi dòng lấy ra các thông tin sau:<br>STT;<br>Mã vùng;<br>Tên vùng;<br>Trước thuế:<br>Doanh thu thực hiện (USD);<br>Doanh thu kế hoạch (USD);<br>Tỷ lệ hoàn thành doanh thu (%);<br>Sau thuế:<br>Doanh thu thực hiện (USD);<br>Doanh thu kế hoạch (USD);<br>Tỷ lệ hoàn thành doanh thu (%);<br>Sắp xếp theo (SX1).|

- Tra cứu theo tỉnh:

<img src="media/image37.png" id="image33">

| # | # |
|---|---|
|Đầu vào|(BL1) Từ khóa: Chuỗi 0-255 ký tự, không chứa khoảng cách đầu cuối;<br>(BL2) Kỳ báo cáo: Bắt buộc, chọn 01 kỳ báo cáo trong danh sách;<br>(BL3) Vùng: Chọn 01 vùng trong danh sách;<br>(SX1) Chọn trong danh sách bao gồm:<br>Theo mã tỉnh (A→Z);|
|Đầu ra|Lấy ra tất cả các tỉnh thỏa mãn, tiêu chí nào để trống thì coi như thỏa mãn:<br>Có tên chứa (BL1) hoặc mã = (BL1) không phân biệt hoa thường, dấu;<br>Được tính tỷ lệ hoàn thành doanh thu trong kỳ báo cáo (BL2);<br>Thuộc vùng (BL3);<br>Mỗi dòng lấy ra các thông tin sau:<br>STT;<br>Mã vùng;<br>Mã tỉnh;<br>Tên tỉnh;<br>Trước thuế:<br>Doanh thu thực hiện (USD);<br>Doanh thu kế hoạch (USD);<br>Tỷ lệ hoàn thành doanh thu (%);<br>Sau thuế:<br>Doanh thu thực hiện (USD);<br>Doanh thu kế hoạch (USD);<br>Tỷ lệ hoàn thành doanh thu (%);<br>Sắp xếp theo (SX1).|

- Theo bưu cục:

<img src="media/image38.png" id="image34">

| # | # |
|---|---|
|Đầu vào|(BL1) Từ khóa: Chuỗi 0-255 ký tự, không chứa khoảng cách đầu cuối;<br>(BL2) Kỳ báo cáo: Bắt buộc, chọn 01 kỳ báo cáo trong danh sách;<br>(BL3) Vùng: Chọn 01 vùng trong danh sách;<br>(BL4) Tỉnh: Chọn 01 tỉnh trong danh sách;<br>(SX1) Chọn trong danh sách bao gồm:<br>Theo mã vùng (A→Z);|
|Đầu ra|Lấy ra tất cả các bưu cục thỏa mãn, tiêu chí nào để trống thì coi như thỏa mãn:<br>Có tên chứa (BL1) hoặc mã = (BL1) không phân biệt hoa thường, dấu;<br>Được tính tỷ lệ hoàn thành doanh thu trong kỳ báo cáo (BL2);<br>Thuộc vùng (BL3);<br>Thuộc tỉnh (BL4);<br>Mỗi dòng lấy ra các thông tin sau:<br>STT;<br>Mã vùng;<br>Mã tỉnh;<br>Mã bưu cục;<br>Tên bưu cục;<br>Trước thuế:<br>Doanh thu thực hiện (USD);<br>Doanh thu kế hoạch (USD);<br>Tỷ lệ hoàn thành doanh thu (%);<br>Sau thuế:<br>Doanh thu thực hiện (USD);<br>Doanh thu kế hoạch (USD);<br>Tỷ lệ hoàn thành doanh thu (%);<br>Sắp xếp theo (SX1).|

### Tra cứu app
#### Tra cứu thù lao nhân viên trên app

18.04.2026 Điều chỉnh:

LV1: Hiện thêm số chuyến xe vào sản lượng;

LV2: Điều chỉnh số lượng cấu phần lương;

LV3: Bổ sung mô tả về tên giao dịch & loại sự kiện khi sự kiện = hoàn thành chuyến xe;

LV4: Bổ sung màn chi tiết chuyến xe.

25.04.2026

Bổ sung các màn chi tiết hiển thị lương khách hàng mới, lương cứng, lương hoàn thành KPI, lương khai thác;

Bổ sung kiểm tra khi tra cứu lương:

Nếu người dùng thuộc bưu cục loại đại lý → Tra cứu hoa hồng đại lý;

Khác → Tra cứu thù lao nhân viên.

| # | # |
|---|---|
|Use Case|Tra cứu thù lao trên app|
|Use Case ID||
|Description|Tra cứu thù lao trên app|
|Actor|Nhân viên bưu tá, nhân viên đại lý|
|Pre-Condition|User đăng nhập thành công vào ứng dụng metfone nội bộ.|
|Trigger|Unitel → Trang chủ → Thu nhập → Chọn 1 ngày|
|Post-Condition|Tra cứu được thù lao của bản thân.|
|Priority|High|
|Flow|1. Tra cứu tổng quan;<br>2. Tra cứu chi tiết tới từng phần tử lương;<br>3. Tra cứu chi tiết tới từng giao dịch;<br>4. Xem chi tiết 1 giao dịch.|
|Business Rule|BR01. Kiểm tra tính hợp lệ của bộ lọc.<br>BR02. Quy tắc tìm kiếm:<br>BR04. Sắp xếp: Chọn 1 trong các lựa chọn:<br>Theo tên nhân viên (A→Z);<br>BR05. Phân trang: 100 bản ghi/trang.|

LV1:

<img src="media/image39.png" id="image35">

| # | # | # |
|---|---|---|
|Đầu vào|(BL1) Thời gian:<br>Hôm nay: Ngày hiện tại;<br>Hôm qua: Ngày hiện tại – 1 ngày;<br>Tuần này: Thứ 2 tuần hiện tại – Ngày hiện tại;<br>Tuần trước: Thứ 2 tới CN tuần hiện tại – 1;<br>Tháng này: Ngày 1 tới ngày hiện tại, tháng hiện tại (Mặc định);<br>Tháng trước: Ngày 1 tới ngày cuối tháng hiện tại – 1;<br>Khác: Cho phép người dùng thiết lập kỳ lọc tối đa 31 ngày.<br>(BL2) Nhân viên: Người đang đăng nhập;<br>(BL3) Bưu cục: Bưu cục đang đăng nhập.||
|Đầu ra|Bưu cục thường|Đại lý|
||(KQ1) Tổng thu nhập: Tổng các khoản thù lao t/m:<br>Ngày khoán thuộc kỳ (BL1);<br>Nhân viên hưởng = (BL2);<br>Bưu cục hưởng = (BL3);<br>(KQ2) Tổng hợp sản lượng:<br>Giao hàng: Số mã vận đơn được nhân viên (BL2) giao tại bưu cục (BL3) trong khoảng (BL1);<br>Nhận hàng: Số mã vận đơn dược nhân viên (BL2) nhận tại bưu cục (BL3) trong khoảng (BL1);<br>Chuyến xe: Số mã chuyến xe được nhân viên (BL2) hoàn thành tại bưu cục (BL3) trong khoảng (BL1);<br>(KQ3) Chi tiết lương từng ngày:<br>Bao gồm: Danh sách ngày thuộc kỳ (BL1);<br>Mỗi ngày lấy ra:<br>(KQ3.1) Ngày theo định dạng dd/mm/yyyy;<br>(KQ3.2) Thu nhập trong ngày: Tổng giá trị các giao dịch t/m:<br>Ngày khoán = (KQ3.1);<br>Nhân viên hưởng = (BL2);<br>Bưu cục hưởng = (BL3);<br>→ Thao tác: Chọn 1 ngày để xem chi tiết → Chuyển sang bước 2.|(KQ1) Tổng thu nhập: Tổng các khoản thù lao t/m:<br>Ngày khoán thuộc kỳ (BL1);<br>Bưu cục hưởng = (BL3);<br>(KQ2) Tổng hợp sản lượng:<br>Giao hàng: Số mã vận đơn được giao tại bưu cục (BL3) trong khoảng (BL1);<br>Nhận hàng: Số mã vận đơn được nhận tại bưu cục (BL3) trong khoảng (BL1);<br>Chuyến xe: Số mã chuyến xe được hoàn thành tại bưu cục (BL3) trong khoảng (BL1);<br>(KQ3) Chi tiết lương từng ngày:<br>Bao gồm: Danh sách ngày thuộc kỳ (BL1);<br>Mỗi ngày lấy ra:<br>(KQ3.1) Ngày theo định dạng dd/mm/yyyy;<br>(KQ3.2) Thu nhập trong ngày: Tổng giá trị các giao dịch t/m:<br>Ngày khoán = (KQ3.1);<br>Bưu cục hưởng = (BL3);<br>→ Thao tác: Chọn 1 ngày để xem chi tiết → Chuyển sang bước 2.|

LV2:

<img src="media/image40.png" id="image36"> <img src="media/image41.png" id="image37">

| # | # | # |
|---|---|---|
|Đầu vào|(BL1) Thời gian: Bao gồm:<br>Hôm nay: Ngày hiện tại;<br>Hôm qua: Ngày hiện tại – 1 ngày;<br>Tuần này: Thứ 2 tuần hiện tại – Ngày hiện tại;<br>Tuần trước: Thứ 2 tới CN tuần hiện tại – 1;<br>Tháng này: Ngày 1 tới ngày hiện tại, tháng hiện tại;<br>Tháng trước: Ngày 1 tới ngày cuối tháng hiện tại – 1;<br>Khác: Cho phép người dùng thiết lập kỳ lọc tối đa 31 ngày, mặc định chọn ngày được chọn ở bước 1.<br>(BL2) Nhân viên: Người đang đăng nhập;<br>(BL3) Bưu cục: Bưu cục đang đăng nhập;||
|Đầu ra|Bưu cục thường|Đại lý|
||(KQ1) Tổng thu nhập: Tổng các khoản thù lao t/m:<br>Ngày khoán thuộc kỳ (BL1);<br>Nhân viên hưởng = (BL2);<br>Bưu cục hưởng = (BL3);<br>(KQ2) Tổng hợp sản lượng:<br>Giao hàng: Số mã vận đơn được nhân viên (BL2) giao tại bưu cục (BL3) trong khoảng (BL1);<br>Nhận hàng: Số mã vận đơn dược nhân viên (BL2) nhận tại bưu cục (BL3) trong khoảng (BL1);<br>Chuyến xe: Số mã chuyến xe được nhân viên (BL2) hoàn thành tại bưu cục (BL3) trong khoảng (BL1);<br>(KQ3) Chi tiết lương theo cấu phần:<br>Bao gồm:<br>Lương cứng;<br>Lương khoán;<br>Hoàn thành KPI;<br>Giao hàng;<br>Nhận hàng;<br>Khai thác;<br>Kết nối;<br>Khách hàng mới;<br>Phụ cấp;<br>Thưởng phạt;<br>Khác (Bao gồm các phần tử không thuộc danh sách kể trên);<br>Mỗi loại lấy ra:<br>(KQ5.1) Loại lương;<br>(KQ5.2) Tổng thù lao của các phần tử;<br>(KQ5.3) Chi tiết lương mỗi phần tử:<br>Lấy ra danh sách phần tử lương thuộc loại (KQ5.1);<br>Mỗi phần tử lấy ra:<br>(KQ5.3.1) Mã phần tử;<br>(KQ5.3.2) Tên phần tử;<br>(KQ5.3.3) Phân loại;<br>(KQ5.3.4) Tổng thù lao thỏa mãn;<br>Ngày khoán thuộc kỳ (BL1);<br>Do nhân viên (BL2) giao;<br>Do bưu cục (BL3) giao;<br>Phần tử lương = (KQ5.3.1)<br>(KQ5.3.5) Thao tác: Chọn 1 phần tử lương để xem chi tiết tiếp → Chuyển sang cấp 3.|(KQ1) Tổng thu nhập: Tổng các khoản thù lao t/m:<br>Ngày khoán thuộc kỳ (BL1);<br>Bưu cục hưởng = (BL3);<br>(KQ2) Tổng hợp sản lượng:<br>Giao hàng: Số mã vận đơn được giao tại bưu cục (BL3) trong khoảng (BL1);<br>Nhận hàng: Số mã vận đơn được nhận tại bưu cục (BL3) trong khoảng (BL1);<br>Chuyến xe: Số mã chuyến xe được hoàn thành tại bưu cục (BL3) trong khoảng (BL1);<br>(KQ3) Chi tiết lương theo cấu phần:<br>Bao gồm:<br>Hoa hồng giao;<br>Hoa hồng nhận;<br>Khác (Bao gồm các phần tử không thuộc danh sách kể trên);<br>Mỗi loại lấy ra:<br>(KQ5.1) Loại lương;<br>(KQ5.2) Tổng thù lao của các phần tử;<br>(KQ5.3) Chi tiết lương mỗi phần tử:<br>Lấy ra danh sách phần tử lương thuộc loại (KQ5.1);<br>Mỗi phần tử lấy ra:<br>(KQ5.3.1) Mã phần tử;<br>(KQ5.3.2) Tên phần tử;<br>(KQ5.3.3) Phân loại;<br>(KQ5.3.4) Tổng thù lao thỏa mãn;<br>Ngày khoán thuộc kỳ (BL1);<br>Do bưu cục (BL3) giao;<br>Phần tử lương = (KQ5.3.1)<br>(KQ5.3.5) Thao tác: Chọn 1 phần tử lương để xem chi tiết tiếp → Chuyển sang cấp 3.|

LV3:

<img src="media/image42.png" id="image38">

| # | # | # |
|---|---|---|
|Đầu vào|(BL1) Thời gian: Bao gồm:<br>Hôm nay: Ngày hiện tại;<br>Hôm qua: Ngày hiện tại – 1 ngày;<br>Tuần này: Thứ 2 tuần hiện tại – Ngày hiện tại;<br>Tuần trước: Thứ 2 tới CN tuần hiện tại – 1;<br>Tháng này: Ngày 1 tới ngày hiện tại, tháng hiện tại;<br>Tháng trước: Ngày 1 tới ngày cuối tháng hiện tại – 1;<br>Khác: Cho phép người dùng thiết lập kỳ lọc tối đa 31 ngày, mặc định chọn ngày được chọn ở bước 2.<br>(BL2) Nhân viên: Người đang đăng nhập;<br>(BL3) Bưu cục: Bưu cục đang đăng nhập;<br>(BL4) Phần tử lương: Phần tử được chọn ở bước 2.||
|Đầu ra|Bưu cục thường|Đại lý|
||(KQ1) Tổng thu nhập: Tổng các khoản thù lao t/m:<br>Ngày khoán thuộc kỳ (BL1);<br>Nhân viên hưởng = (BL2);<br>Bưu cục hưởng = (BL3);<br>Thuộc phần tử (BL4);<br>(KQ2) Chi tiết giao dịch:<br>Bao gồm các giao dịch thỏa mãn:<br>Ngày khoán thuộc kỳ (BL1);<br>Do nhân viên (BL2) giao;<br>Do bưu cục (BL3) giao;<br>Thuộc phần tử (BL4);<br>Mỗi giao dịch lấy ra:<br>(KQ2.1) Tên giao dịch:<br>Với phần tử tự động:<br>Sự kiện giao/nhận: Mã phiếu gửi (VD. VTP123456789123);<br>Sự kiện hoàn thành chuyến xe: mã chuyến xe (VD. CX005238490);<br>Sự kiện khách hàng mới: ID khách hàng (VD. 12325454);<br>Sự kiện lương cứng / chốt tỷ lệ hoàn thành KPI / Khai thác: MM/YYYY của ngày khoán (VD. 08/2026).<br>Với phần tử thủ công: Ngày khoán;<br>(KQ2.2) Tên loại sự kiện phát sinh giao dịch:<br>Bao gồm:<br>Giao hàng;<br>Nhận hàng;<br>Hoàn thành chuyến xe;<br>Khách hàng mới;<br>Lương cứng;<br>Chốt tỷ lệ hoàn thành KPI;<br>Khai thác.<br>Chỉ hiển thị với phần tử tự động;<br>(KQ2.3) Thời gian phát sinh giao dịch;<br>(KQ2.4) Số tiền được cộng/trừ vào từ giao dịch;<br>→ Thao tác: Chọn 1 giao dịch để xem chi tiết → Chuyển bước 4.|(KQ1) Tổng thu nhập: Tổng các khoản thù lao t/m:<br>Ngày khoán thuộc kỳ (BL1);<br>Bưu cục hưởng = (BL3);<br>Thuộc phần tử (BL4);<br>(KQ2) Chi tiết giao dịch:<br>Bao gồm các giao dịch thỏa mãn:<br>Ngày khoán thuộc kỳ (BL1);<br>Do bưu cục (BL3) giao;<br>Thuộc phần tử (BL4);<br>Mỗi giao dịch lấy ra:<br>(KQ2.1) Tên giao dịch:<br>Với phần tử tự động:<br>Sự kiện giao/nhận: Mã phiếu gửi (VD. VTP123456789123);<br>Sự kiện hoàn thành chuyến xe: mã chuyến xe (VD. CX005238490);<br>Sự kiện khách hàng mới: ID khách hàng (VD. 12325454);<br>Sự kiện lương cứng / chốt tỷ lệ hoàn thành KPI / Khai thác: MM/YYYY của ngày khoán (VD. 08/2026).<br>Với phần tử thủ công: Ngày khoán;<br>(KQ2.2) Tên loại sự kiện phát sinh giao dịch:<br>Bao gồm:<br>Giao hàng;<br>Nhận hàng;<br>Hoàn thành chuyến xe;<br>Khách hàng mới;<br>Lương cứng;<br>Chốt tỷ lệ hoàn thành KPI;<br>Khai thác.<br>Chỉ hiển thị với phần tử tự động;<br>(KQ2.3) Thời gian phát sinh giao dịch;<br>(KQ2.4) Số tiền được cộng/trừ vào từ giao dịch;<br>→ Thao tác: Chọn 1 giao dịch để xem chi tiết → Chuyển bước 4.|

LV4:

<img src="media/image43.png" id="image39">

| # | # |
|---|---|
|Đầu vào|(BL1) Giao dịch: Được chọn để xem chi tiết ở B3.|
|Đầu ra|(KQ1) Thông tin chung<br>(KQ1.1) Ngày báo cáo;<br>(KQ1.2) Số tiền;<br>(KQ1.3) Thời gian cập nhật giao dịch;<br>(KQ2) Thông tin chi tiết<br>TH1: Phần tử tính tự động:<br>Tên phân loại sự kiện: Giao hàng / Nhận hàng / Hoàn thành chuyến xe;<br>Thông tin chi tiết sự kiện → Tham chiếu bảng mô tả dưới đây;<br>TH2: Phần tử tính thủ công:<br>Người duyệt file nhập liệu (VD. Nguyễn Văn An (annv1);<br>Thời gian nhập liệu.|

 Sự kiện _ Thông tin hiển thị

| # | # | # | # |
|---|---|---|---|
|STT|Loại sự kiện|Trường dữ liệu|Mô tả|
|1|Giao, nhận hàng|Mã phiếu gửi||
|2|Giao, nhận hàng|Thời gian||
|3|Giao, nhận hàng|Bưu cục gốc||
|4|Giao, nhận hàng|Bưu cục phát||
|5|Giao, nhận hàng|Dịch vụ chính||
|6|Giao, nhận hàng|Dịch vụ khác||
|7|Giao, nhận hàng|Loại hàng hóa|GOODS: Hàng hóa;<br>DOCUMENT: Thư.|
|8|Giao, nhận hàng|Trọng lượng|Đơn vị: gram|
|9|Giao, nhận hàng|Cước trước thuế|Đơn vị: USD|
|10|Giao, nhận hàng|Cước sau thuế|Đơn vị: USD|
|11|Giao, nhận hàng|Thu hộ|Đơn vị: USD|
|12|Giao, nhận hàng|Người giới thiệu||
|13|Hoàn thành chuyến xe|Mã chuyến xe|Mã chuyến xe (VD. CX005238490)|
|14|Hoàn thành chuyến xe|Mã đơn vị vận chuyển|Mã bưu cục.|
|15|Hoàn thành chuyến xe|Mã hành trình|Mã hành trình.|
|16|Hoàn thành chuyến xe|Loại hành trình|Mã loại hành trình.|
|17|Hoàn thành chuyến xe|Chiều|Tên chiều, bao gồm:<br>1: Chiều đi;<br>2: Chiều về.|
|18|Hoàn thành chuyến xe|Tên tuyến|Tên tuyến.|
|19|Hoàn thành chuyến xe|Biển số xe|Biển số xe.|
|20|Hoàn thành chuyến xe|Loại sở hữu|Tên loại sở hữu.|
|21|Hoàn thành chuyến xe|Loại phương tiện|Tên loại phương tiện.|
|22|Hoàn thành chuyến xe|Đối tác|Tên đối tác.|
|23|Hoàn thành chuyến xe|Trọng tải|Trọng tải của xe, đơn vị: kg.|
|24|Hoàn thành chuyến xe|Sản lượng|Sản lượng của chuyến (đơn vị: chiếc), bao gồm:<br>Sản lượng tải;<br>Sản lượng kiện;<br>Tổng sản lượng tải + kiện.|
|25|Hoàn thành chuyến xe|Trọng lượng|Trọng lượng của chuyến, đơn vị: kg, bao gồm:<br>Trọng lượng tải;<br>Trọng lượng kiện;<br>Tổng trọng lượng tải + kiện.|
|26|Hoàn thành chuyến xe|Quãng đường di chuyển|Quãng đường di chuyển, bao gồm:<br>Hành trình , đơn vị: km;<br>Tài xế nhập, đơn vị: km;<br>GPS, đơn vị: km;<br>Loại quãng đường được phê duyệt: ”Hành trình” / ”Tài xế nhập” / ”GPS”.|
|27|Hoàn thành chuyến xe|Hiệu quả|Hiệu quả xe, đơn vị: %|
|28|Hoàn thành chuyến xe|Tài xế|Danh sách tài xế thực hiện chuyến.<br>Định dạng: <Họ và tên> (<MNV>);<br>Bao gồm:<br>Tài xế 1;<br>Tài xế 2.|
|29|Hoàn thành chuyến xe|Thời gian|Thời gian của chuyến xe.<br>Định dạng: HH:MM dd/MM/yyyy;<br>Bao gồm:<br>Bắt đầu;<br>Kết thúc.|
|30|Khách hàng mới|ID Khách hàng|ID Khách hàng.|
|31|Khách hàng mới|Tên khách hàng|Tên khách hàng.|
|32|Khách hàng mới|Ngày phát sinh|Ngày phát sinh, định dạng dd/MM/yyyy,|
|33|Khách hàng mới|Số tháng doanh thu|Số tháng doanh thu, đơn vị: tháng.|
|34|Khách hàng mới|Doanh thu tháng phát sinh|Doanh thu tháng phát sinh, hiện 2 chữ số thập phân, đơn vị: USD.|
|35|Khách hàng mới|Tháng báo cáo|Tháng báo cáo, định dạng MM/yyyy.|
|36|Khách hàng mới|Doanh thu tháng báo cáo|Doanh thu tháng báo cáo, hiện 2 chữ số thập phân, đơn vị: USD.|
|37|Khách hàng mới|Giảm giá tháng báo cáo|Giảm giá tháng báo cáo, hiện 2 chữ số thập phân, đơn vị: USD.|
|38|Khách hàng mới|Tỷ lệ hưởng|Tỷ lệ hưởng = Tiền lương được hưởng /  Doanh thu tháng báo cáo * 1000%.|
|39|Khách hàng mới|Nhân viên giới thiệu|Nhân viên giới thiệu, định dạng: <Họ và tên> (<MNV>).|
|40|Lương cứng|Nhân viên|Nhân viên hưởng lương khai thác, định dạng: <Họ và tên> (<MNV>).|
|41|Lương cứng|Bưu cục|Mã bưu cục của nhân viên hưởng.|
|42|Lương cứng|Chức danh|Tên chức danh của nhân viên hưởng.|
|43|Lương cứng|Số ngày nghỉ|Số ngày nghỉ trong tháng, đơn vị: ngày.|
|44|Lương cứng|Lương HAY|Lương HAY của nhân viên, hiện 2 chữ số thập phân, đơn vị: USD.|
|45|Lương cứng|Tỷ lệ hoàn thành doanh thu cá nhân|Tỷ lệ hoàn thành doanh thu vùng, hiện 2 chữ số thập phân, đơn vị: %.|
|46|Khai thác|Nhân viên|Nhân viên hưởng lương khai thác, định dạng: <Họ và tên> (<MNV>).|
|47|Khai thác|Bưu cục|Mã bưu cục của nhân viên hưởng.|
|48|Khai thác|Chức danh|Tên chức danh của nhân viên hưởng.|
|49|Khai thác|Tỷ lệ hoàn thành doanh thu tổng|Tỷ lệ hoàn thành doanh thu tổng, hiện 2 chữ số thập phân, đơn vị: %, bao gồm:<br>Trước thuế;<br>Sau thuế.|
|50|Chốt KPI|Nhân viên|Nhân viên hưởng lương khai thác, định dạng: <Họ và tên> (<MNV>).|
|51|Chốt KPI|Bưu cục|Mã bưu cục của nhân viên hưởng.|
|52|Chốt KPI|Chức danh|Tên chức danh của nhân viên hưởng.|
|53|Chốt KPI|Tỷ lệ hoàn thành doanh thu bưu cục|Tỷ lệ hoàn thành doanh thu bưu cục, hiện 2 chữ số thập phân, đơn vị: %, bao gồm:<br>Trước thuế;<br>Sau thuế.|
|54|Chốt KPI|Tỷ lệ hoàn thành doanh thu tỉnh|Tỷ lệ hoàn thành doanh thu tỉnh, hiện 2 chữ số thập phân, đơn vị: %, bao gồm:<br>Trước thuế;<br>Sau thuế.|
|55|Chốt KPI|Tỷ lệ hoàn thành doanh thu vùng|Tỷ lệ hoàn thành doanh thu vùng, hiện 2 chữ số thập phân, đơn vị: %, bao gồm:<br>Trước thuế;<br>Sau thuế.|
|55|Chốt KPI|Tỷ lệ hoàn thành doanh thu tổng|Tỷ lệ hoàn thành doanh thu tổng, hiện 2 chữ số thập phân, đơn vị: %, bao gồm:<br>Trước thuế;<br>Sau thuế.|
|56|Chốt KPI|Tỷ lệ hoàn thành doanh thu cá nhân|Tỷ lệ hoàn thành doanh thu vùng, hiện 2 chữ số thập phân, đơn vị: %.|
|57|Chốt KPI|Lương HAY|Lương HAY của nhân viên, hiện 2 chữ số thập phân, đơn vị: USD.|

# THIẾT KẾ PHI CHỨC NĂNG
# PHỤ LỤC

PL1. Hiển thị thông tin chi tiết trên web

| # | # | # | # |
|---|---|---|---|
|STT|Sự kiện|Trường dữ liệu|Key tương ứng trong topic Kafka|
|1|Giao hàng, Nhận hàng|Mã phiếu gửi||
|2|Giao hàng, Nhận hàng|Thời gian tác động||
|3|Giao hàng, Nhận hàng|Bưu cục gốc||
|4|Giao hàng, Nhận hàng|Bưu cục phát||
|5|Giao hàng, Nhận hàng|Dịch vụ chính||
|6|Giao hàng, Nhận hàng|Dịch vụ khác||
|7|Giao hàng, Nhận hàng|Loại hàng hóa||
|8|Giao hàng, Nhận hàng|Trọng lượng (gram)||
|9|Giao hàng, Nhận hàng|Cước trước thuế (USD)||
|10|Giao hàng, Nhận hàng|Cước sau thuế (USD)||
|11|Giao hàng, Nhận hàng|Thu hộ||
|12|Giao hàng, Nhận hàng|Người tác động||
|13|Giao hàng, Nhận hàng|Người giới thiệu||
|14|Hoàn thành chuyến xe|Mã chuyến xe|tripCode|
|15|Hoàn thành chuyến xe|Đơn vị vận chuyển|organizationCode|
|16|Hoàn thành chuyến xe|Mã hành trình|routeCode|
|17|Hoàn thành chuyến xe|Loại hành trình|routeTypeCode|
|18|Hoàn thành chuyến xe|Chiều|direction<br>1 - ”Chiều đi”;<br>2 - ”Chiều về”|
|19|Hoàn thành chuyến xe|Tên tuyến|roadName|
|20|Hoàn thành chuyến xe|Biển số xe|vehiclePlate|
|21|Hoàn thành chuyến xe|Loại sở hữu|vehicleSourceName|
|22|Hoàn thành chuyến xe|Loại phương tiện|vehicleTypeName|
|23|Hoàn thành chuyến xe|Đối tác|partnerName|
|24|Hoàn thành chuyến xe|Trọng tải (KG)|capacity|
|25|Hoàn thành chuyến xe|Sản lượng – Tải|bagVolume|
|26|Hoàn thành chuyến xe|Sản lượng – Kiện|packageVolume|
|27|Hoàn thành chuyến xe|Trọng lượng – Tải|bagWeight|
|28|Hoàn thành chuyến xe|Trọng lượng – Kiện|packageWeight|
|29|Hoàn thành chuyến xe|Trọng lượng – Tổng|weight|
|30|Hoàn thành chuyến xe|Khoảng cách – Hành trình|plannedDistance|
|31|Hoàn thành chuyến xe|Khoảng cách – Tài xế nhập|reportedDistance|
|32|Hoàn thành chuyến xe|Khoảng cách – GPS|actualDistance|
|33|Hoàn thành chuyến xe|Khoảng cách – Phê duyệt|approvedDistanceType<br>”PLANNED” – Hành trình;<br>”REPORTED” – Tài xế nhập;<br>”GPS” – GPS;|
|34|Hoàn thành chuyến xe|Hiệu quả (%)|efficency|
|35|Hoàn thành chuyến xe|Danh sách tài xế - Tài xế 1|Lấy ra họ tên & mã nhân viên của userid trong key drivers.|
|36|Hoàn thành chuyến xe|Danh sách tài xế - Tài xế 2|Lấy ra họ tên & mã nhân viên của userid trong key drivers.|
|37|Hoàn thành chuyến xe|Thời gian|Hh:mm dd/mm/yyy, bao gồm:<br>Bắt đầu: startTime;<br>Kết thúc: endTime.|
|38|Khách hàng mới|ID Khách hàng|cusID|
|39|Khách hàng mới|Tháng khoán|reportMonth|
|40|Khách hàng mới|Tên khách hàng|cusName|
|41|Khách hàng mới|Ngày phát sinh doanh thu|firstRevDate|
|42|Khách hàng mới|Số tháng doanh thu|revMonths|
|43|Khách hàng mới|Doanh thu tháng phát sinh|firstMonthRev|
|44|Khách hàng mới|Doanh thu tháng báo cáo|MonthRev|
|45|Khách hàng mới|Giảm giá tháng báo cáo|MonthDisc|
|46|Khách hàng mới|Nhân viên giới thiệu|userIdReferrer|
|47|Khách hàng mới|Tỷ lệ hưởng|Thành tiền / MonthRev * 100, làm tròn tới số thập phân thứ 2.|
|48|Lương cứng|Chức danh|Tên chức danh.|
|49|Lương cứng|Số ngày nghỉ (ngày)|Số ngày nghỉ (đơn vị: ngày)|
|50|Lương cứng|Tỷ lệ hoàn thành KPI cá nhân (%)||
|51|Lương cứng|Lương hay (USD)||
|52|Khai thác|Tỷ lệ hoàn thành doanh thu tổng trước thuế (%)||
|53|Khai thác|Tỷ lệ hoàn thành doanh thu tổng sau thuế (%)||
|54|Chốt tỷ lệ hoàn thành KPI|Chức danh||
|55|Chốt tỷ lệ hoàn thành KPI|Tỷ lệ hoàn thành KPI cá nhân (%)||
|56|Chốt tỷ lệ hoàn thành KPI|Tỷ lệ hoàn thành doanh thu bưu cục trước thuế (%)||
|57|Chốt tỷ lệ hoàn thành KPI|Tỷ lệ hoàn thành doanh thu bưu cục sau thuế (%)||
|58|Chốt tỷ lệ hoàn thành KPI|Tỷ lệ hoàn thành doanh thu tỉnh trước thuế (%)||
|59|Chốt tỷ lệ hoàn thành KPI|Tỷ lệ hoàn thành doanh thu tỉnh sau thuế (%)||
|60|Chốt tỷ lệ hoàn thành KPI|Tỷ lệ hoàn thành doanh thu vùng trước thuế (%)||
|61|Chốt tỷ lệ hoàn thành KPI|Tỷ lệ hoàn thành doanh thu vùng sau thuế (%)||
|62|Chốt tỷ lệ hoàn thành KPI|Tỷ lệ hoàn thành doanh thu tổng trước thuế (%)||
|63|Chốt tỷ lệ hoàn thành KPI|Tỷ lệ hoàn thành doanh thu tổng sau thuế (%)||