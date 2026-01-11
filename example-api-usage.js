// Пример использования API из рендер-процесса (фронтенд)
// Этот код можно использовать в React-компонентах для взаимодействия с Python-бэкендом

class ApiService {
  // Получение данных с бэкенда
  static async getData(endpoint) {
    try {
      const response = await window.electronAPI.sendRequest('GET', endpoint, null);
      return response;
    } catch (error) {
      console.error('Ошибка при получении данных:', error);
      throw error;
    }
  }

  // Отправка данных на бэкенд
  static async postData(endpoint, data) {
    try {
      const response = await window.electronAPI.sendRequest('POST', endpoint, data);
      return response;
    } catch (error) {
      console.error('Ошибка при отправке данных:', error);
      throw error;
    }
  }

  // Пример вызова API для получения главной страницы
  static async getRootData() {
    return await this.getData('/');
  }

  // Пример вызова специфичного эндпоинта
  static async getGprData() {
    return await this.getData('/gpr/some-endpoint'); // заменить на реальный эндпоинт
  }
}

// Пример использования в компоненте React
/*
import React, { useEffect, useState } from 'react';

function App() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const result = await ApiService.getRootData();
        setData(result);
      } catch (error) {
        console.error('Failed to fetch data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return <div>Загрузка...</div>;
  }

  return (
    <div>
      <h1>Строд-Сервис Технолоджи</h1>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}
*/

export default ApiService;