// Типы данных для ГПР (График Производства Работ)

export interface GPRRecord {
  id: string;
  customerId: string;
  objectId: string;
  workType: string; // Тип работ (материал исполнения)
  volumePlan: number; // Объем планируемых работ
  volumeFact: number; // Объем фактически выполненных работ
  volumeRemainder: number; // Остаток объема
  progress: number; // Процент выполнения
  dailyData: Record<string, number>; // Ежедневные данные (ключ - дата в формате YYYY-MM-DD)
  createdAt: string;
  updatedAt?: string;
}

export interface CreateGPRRecordRequest {
  customerId: string;
  objectId: string;
  workType: string;
  volumePlan: number;
  volumeFact: number;
  dailyData?: Record<string, number>;
}

export interface UpdateGPRRecordRequest {
  customerId?: string;
  objectId?: string;
  workType?: string;
  volumePlan?: number;
  volumeFact?: number;
  dailyData?: Record<string, number>;
}

export interface WeeklyReport {
  id: string;
  weekStartDate: string;
  reportData: WeeklyReportData[];
  createdBy: string;
  createdAt: string;
}

export interface WeeklyReportData {
  material: string; // Название материала
  plan: number; // Планируемый объем
  fact: number; // Фактический объем
}

export interface GenerateWeeklyReportRequest {
  weekStartDate: string;
  createdBy: string;
}

export interface WorkTypeOption {
  id: string;
  name: string;
}

// Справочник материалов
export const WORK_TYPE_OPTIONS: WorkTypeOption[] = [
  { id: 'kraska_b', name: 'Краска б' },
  { id: 'kraska_ch', name: 'Краска ч' },
  { id: 'vremyanka', name: 'Времянка' },
  { id: 'kraska_j', name: 'Краска ж' },
  { id: 'hp', name: 'ХП' },
  { id: 'hpj', name: 'ХПж' },
  { id: 'tp', name: 'ТП' },
  { id: 'demarkirovka', name: 'Демаркировка' }
];