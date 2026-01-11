import {
  GPRRecord,
  CreateGPRRecordRequest,
  UpdateGPRRecordRequest,
  WeeklyReport,
  GenerateWeeklyReportRequest,
  WeeklyReportData,
  WORK_TYPE_OPTIONS
} from '../../shared/types/gpr';

// Mock-данные для демонстрации
const mockGPRRecords: GPRRecord[] = [
  {
    id: '1',
    customerId: '1',
    objectId: '1',
    workType: 'kraska_b',
    volumePlan: 100,
    volumeFact: 65,
    volumeRemainder: 35,
    progress: 65,
    dailyData: {
      '2023-06-01': 10,
      '2023-06-02': 15,
      '2023-06-03': 20,
      '2023-06-04': 20
    },
    createdAt: '2023-06-01T00:00:00Z'
  },
  {
    id: '2',
    customerId: '2',
    objectId: '2',
    workType: 'kraska_ch',
    volumePlan: 200,
    volumeFact: 120,
    volumeRemainder: 80,
    progress: 60,
    dailyData: {
      '2023-06-01': 20,
      '2023-06-02': 30,
      '2023-06-03': 35,
      '2023-06-04': 35
    },
    createdAt: '2023-06-01T00:00:00Z'
  },
  {
    id: '3',
    customerId: '1',
    objectId: '2',
    workType: 'vremyanka',
    volumePlan: 150,
    volumeFact: 90,
    volumeRemainder: 60,
    progress: 60,
    dailyData: {
      '2023-06-01': 15,
      '2023-06-02': 25,
      '2023-06-03': 25,
      '2023-06-04': 25
    },
    createdAt: '2023-06-01T00:00:00Z'
  }
];

// Mock-данные для заказчиков
const mockCustomers = [
  { id: '1', name: 'ООО "СтройИнвест"' },
  { id: '2', name: 'АО "МетроСтрой"' }
];

// Mock-данные для объектов
const mockObjects = [
  { id: '1', name: 'Строительство ТЦ "Гранд"', projectId: '1' },
  { id: '2', name: 'Реконструкция моста', projectId: '2' }
];

const gprService = {
  // Получить все записи ГПР
  async getGPRRecords(): Promise<GPRRecord[]> {
    // Имитация задержки сети
    await new Promise(resolve => setTimeout(resolve, 500));
    return mockGPRRecords;
  },

  // Создать новую запись ГПР
  async createGPRRecord(record: CreateGPRRecordRequest): Promise<GPRRecord> {
    await new Promise(resolve => setTimeout(resolve, 500));
    
    const newRecord: GPRRecord = {
      ...record,
      id: String(mockGPRRecords.length + 1),
      volumeRemainder: record.volumePlan - record.volumeFact,
      progress: Math.round((record.volumeFact / record.volumePlan) * 100),
      dailyData: record.dailyData || {},
      createdAt: new Date().toISOString()
    };
    
    mockGPRRecords.push(newRecord);
    return newRecord;
  },

  // Обновить запись ГПР
  async updateGPRRecord(id: string, record: UpdateGPRRecordRequest): Promise<GPRRecord> {
    await new Promise(resolve => setTimeout(resolve, 500));
    
    const index = mockGPRRecords.findIndex(item => item.id === id);
    if (index !== -1) {
      const updatedRecord = {
        ...mockGPRRecords[index],
        ...record,
        volumeRemainder: record.volumePlan 
          ? record.volumePlan - mockGPRRecords[index].volumeFact 
          : mockGPRRecords[index].volumePlan - mockGPRRecords[index].volumeFact,
        progress: record.volumePlan 
          ? Math.round((mockGPRRecords[index].volumeFact / record.volumePlan) * 100)
          : mockGPRRecords[index].progress,
        updatedAt: new Date().toISOString()
      };
      
      mockGPRRecords[index] = updatedRecord;
      return updatedRecord;
    }
    
    throw new Error(`Record with id ${id} not found`);
  },

  // Удалить запись ГПР
  async deleteGPRRecord(id: string): Promise<void> {
    await new Promise(resolve => setTimeout(resolve, 500));
    
    const index = mockGPRRecords.findIndex(item => item.id === id);
    if (index !== -1) {
      mockGPRRecords.splice(index, 1);
    } else {
      throw new Error(`Record with id ${id} not found`);
    }
  },

  // Сгенерировать недельный отчет
  async generateWeeklyReport(request: GenerateWeeklyReportRequest): Promise<WeeklyReport> {
    await new Promise(resolve => setTimeout(resolve, 500));
    
    // Подсчет данных для отчета на основе mock-данных
    const reportData: WeeklyReportData[] = WORK_TYPE_OPTIONS.map(workType => {
      const recordsForType = mockGPRRecords.filter(record => record.workType === workType.id);
      const totalPlan = recordsForType.reduce((sum, record) => sum + record.volumePlan, 0);
      const totalFact = recordsForType.reduce((sum, record) => sum + record.volumeFact, 0);
      
      return {
        material: workType.name,
        plan: totalPlan,
        fact: totalFact
      };
    });
    
    const weeklyReport: WeeklyReport = {
      id: `report_${request.weekStartDate}_${request.createdBy}`,
      weekStartDate: request.weekStartDate,
      reportData,
      createdBy: request.createdBy,
      createdAt: new Date().toISOString()
    };
    
    return weeklyReport;
  },

  // Получить недельный отчет
  async getWeeklyReport(weekStartDate: string): Promise<WeeklyReport> {
    await new Promise(resolve => setTimeout(resolve, 500));
    
    // Генерируем отчет на основе текущих данных
    const reportData: WeeklyReportData[] = WORK_TYPE_OPTIONS.map(workType => {
      const recordsForType = mockGPRRecords.filter(record => record.workType === workType.id);
      const totalPlan = recordsForType.reduce((sum, record) => sum + record.volumePlan, 0);
      const totalFact = recordsForType.reduce((sum, record) => sum + record.volumeFact, 0);
      
      return {
        material: workType.name,
        plan: totalPlan,
        fact: totalFact
      };
    });
    
    const weeklyReport: WeeklyReport = {
      id: `report_${weekStartDate}_default`,
      weekStartDate,
      reportData,
      createdBy: 'system',
      createdAt: new Date().toISOString()
    };
    
    return weeklyReport;
  }
};

export default gprService;