// Chữ dùng chung trên giao diện.

// Đúng nguyên văn output_guard.DISCLAIMER ở backend.
export const DISCLAIMER = "Thông tin chỉ mang tính tham khảo, vui lòng tham vấn bác sĩ để cá nhân hóa tầm soát.";

export const TAG_LABEL: Record<string, string> = {
  "tong-quat": "Tổng quát",
  "tim-mach": "Tim mạch",
  "ung-thu": "Tầm soát ung thư",
  "cao-tuoi": "Người cao tuổi",
  "tien-hon-nhan": "Tiền hôn nhân",
  "doanh-nghiep": "Doanh nghiệp",
};

export const CITY_OPTIONS = ["Hà Nội", "TP. Hồ Chí Minh", "Đà Nẵng"];

export const GENDER_LABEL: Record<string, string> = { male: "Nam", female: "Nữ" };

export const CATEGORY_LABEL: Record<string, string> = {
  kham: "Khám lâm sàng",
  "xet-nghiem": "Xét nghiệm",
  "chan-doan-hinh-anh": "Chẩn đoán hình ảnh",
  "tham-do-chuc-nang": "Thăm dò chức năng",
};

// Nhóm hạng mục theo loại, giữ thứ tự xuất hiện.
export function byCategory<T extends { category: string }>(rows: T[]): [string, T[]][] {
  const groups = new Map<string, T[]>();
  for (const r of rows) groups.set(r.category, [...(groups.get(r.category) ?? []), r]);
  return [...groups];
}
