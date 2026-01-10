import axios from 'axios';
import {
  GPRRecord,
  CreateGPRRecordRequest,
  UpdateGPRRecordRequest,
  WeeklyReport,
  GenerateWeeklyReportRequest
} from '../../shared/types/gpr';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const gprService = {
  // Получить все записи ГПР
  async getGPRRecords(): Promise<GPRRecord[]> {
    try {
      const response = await axios.get<GPRRecord[]>(`${API_BASE_URL}/gpr/records`);
      return response.data;
    } catch (error) {
      console.error('Ошибка при получении записей ГПР:', error);
      throw error;
    }
  },

  // Создать новую запись ГПР
  async createGPRRecord(record: CreateGPRRecordRequest): Promise<GPRRecord> {
    try {
      const response = await axios.post<GPRRecord>(`${API_BASE_URL}/gpr/records`, record);
      return response.data;
    } catch (error) {
      console.error('Ошибка при создании записи ГПР:', error);
      throw error;
    }
  },

  // Обновить запись ГПР
  async updateGPRRecord(id: string, record: UpdateGPRRecordRequest): Promise<GPRRecord> {
    try {
      const response = await axios.put<GPRRecord>(`${API_BASE_URL}/gpr/records/${id}`, record);
      return response.data;
    } catch (error) {
      console.error('Ошибка при обновлении записи ГПР:', error);
      throw error;
    }
  },

  // Удалить запись ГПР
  async deleteGPRRecord(id: string): Promise<void> {
    try {
      await axios.delete(`${API_BASE_URL}/gpr/records/${id}`);
    } catch (error) {
      console.error('Ошибка при удалении записи ГПР:', error);
      throw error;
    }
  },

  // Сгенерировать недельный отчет
  async generateWeeklyReport(request: GenerateWeeklyReportRequest): Promise<WeeklyReport> {
    try {
      const response = await axios.post<WeeklyReport>(
        `${API_BASE_URL}/gpr/weekly-report`,
        {},
        {
          params: {
            week_start_date: request.weekStartDate,
            created_by: request.createdBy
          }
        }
      );
      return response.data;
    } catch (error) {
      console.error('Ошибка при генерации недельного отчета:', error);
      throw error;
    }
  },

  // Получить недельный отчет
  async getWeeklyReport(weekStartDate: string): Promise<WeeklyReport> {
    try {
      const response = await axios.get<WeeklyReport>(
        `${API_BASE_URL}/gpr/weekly-report/${weekStartDate}`
      );
      return response.data;
    } catch (error) {
      console.error('Ошибка при получении недельного отчета:', error);
      throw error;
    }
  }
};

export default gprService;