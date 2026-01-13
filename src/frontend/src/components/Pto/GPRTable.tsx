import React, { useState, useEffect } from 'react';
import {
  DataGrid,
  GridColDef,
  GridRenderCellParams,
  GridValueGetterParams,
  GridCellEditCommitParams
} from '@mui/x-data-grid';
import {
  Box,
  Paper,
  Typography,
  LinearProgress,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  TextField,
  Button,
  Alert
} from '@mui/material';
import gprService from '../../services/gprService';
import {
  GPRRecord as GPRRecordType,
  WeeklyReportData,
  WORK_TYPE_OPTIONS
} from '@shared/types/gpr';

interface Customer {
  id: string;
  name: string;
}

interface ProjectObject {
  id: string;
  name: string;
  projectId: string;
}

const GPRTable: React.FC = () => {
  const [records, setRecords] = useState<GPRRecordType[]>([]);
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [objects, setObjects] = useState<ProjectObject[]>([]);
  const [selectedWeekStart, setSelectedWeekStart] = useState<string>('');
  const [weeklyReport, setWeeklyReport] = useState<WeeklyReportData[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // Загрузка данных при монтировании компонента
  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        
        // Загрузка записей ГПР
        const gprRecords = await gprService.getGPRRecords();
        setRecords(gprRecords);
      } catch (err) {
        setError('Ошибка при загрузке данных');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const getCustomerName = (id: string) => {
    const customer = customers.find(c => c.id === id);
    return customer ? customer.name : '';
  };

  const getObjectName = (id: string) => {
    const obj = objects.find(o => o.id === id);
    return obj ? obj.name : '';
  };

  const getWorkTypeName = (id: string) => {
    const workType = WORK_TYPE_OPTIONS.find(w => w.id === id);
    return workType ? workType.name : '';
  };

  const calculateRemainder = (plan: number, fact: number) => plan - fact;

  const calculateProgress = (plan: number, fact: number) => {
    if (plan === 0) return 0;
    return Math.round((fact / plan) * 100);
  };

  // Генерация колонок для дней месяца
  const generateDailyColumns = (): GridColDef[] => {
    const columns: GridColDef[] = [];
    const today = new Date();
    const year = today.getFullYear();
    const month = today.getMonth();

    // Получаем количество дней в месяце
    const daysInMonth = new Date(year, month + 1, 0).getDate();

    for (let day = 1; day <= daysInMonth; day++) {
      const dateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
      
      columns.push({
        field: `day_${dateStr}`,
        headerName: `${day}`,
        width: 80,
        renderCell: (params: GridRenderCellParams) => (
          <TextField
            type="number"
            size="small"
            value={params.row.dailyData[dateStr] || ''}
            onChange={(e) => handleDailyDataChange(params.row.id, dateStr, Number(e.target.value))}
            inputProps={{ min: 0 }}
          />
        )
      });
    }

    return columns;
  };

  const handleDailyDataChange = (recordId: string, date: string, value: number) => {
    setRecords(prevRecords =>
      prevRecords.map(record => {
        if (record.id === recordId) {
          const updatedDailyData = { ...record.dailyData, [date]: value };
          const newVolumeFact = Object.values(updatedDailyData).reduce((sum, val) => sum + (val || 0), 0);
          const newVolumeRemainder = calculateRemainder(record.volumePlan, newVolumeFact);
          const newProgress = calculateProgress(record.volumePlan, newVolumeFact);
          
          return {
            ...record,
            dailyData: updatedDailyData,
            volumeFact: newVolumeFact,
            volumeRemainder: newVolumeRemainder,
            progress: newProgress
          };
        }
        return record;
      })
    );
  };

  const columns: GridColDef[] = [
    {
      field: 'customer',
      headerName: 'Заказчик',
      width: 200,
      valueGetter: (params: GridValueGetterParams) => getCustomerName(params.row.customerId),
      editable: true,
      renderEditCell: (params: GridRenderCellParams) => (
        <FormControl size="small" fullWidth>
          <Select
            value={params.row.customerId}
            onChange={(e) => handleFieldChange(params.row.id, 'customerId', e.target.value)}
          >
            {customers.map(customer => (
              <MenuItem key={customer.id} value={customer.id}>
                {customer.name}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
      )
    },
    {
      field: 'object',
      headerName: 'Объект',
      width: 200,
      valueGetter: (params: GridValueGetterParams) => getObjectName(params.row.objectId),
      editable: true,
      renderEditCell: (params: GridRenderCellParams) => (
        <FormControl size="small" fullWidth>
          <Select
            value={params.row.objectId}
            onChange={(e) => handleFieldChange(params.row.id, 'objectId', e.target.value)}
          >
            {objects.map(obj => (
              <MenuItem key={obj.id} value={obj.id}>
                {obj.name}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
      )
    },
    {
      field: 'workType',
      headerName: 'Вид работ',
      width: 150,
      valueGetter: (params: GridValueGetterParams) => getWorkTypeName(params.row.workType),
      editable: true,
      renderEditCell: (params: GridRenderCellParams) => (
        <FormControl size="small" fullWidth>
          <Select
            value={params.row.workType}
            onChange={(e) => handleFieldChange(params.row.id, 'workType', e.target.value)}
          >
            {WORK_TYPE_OPTIONS.map(workType => (
              <MenuItem key={workType.id} value={workType.id}>
                {workType.name}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
      )
    },
    {
      field: 'volumePlan',
      headerName: 'V³ м2 ПЛАН',
      width: 120,
      type: 'number',
      editable: true
    },
    {
      field: 'volumeFact',
      headerName: 'V³ м2 ФАКТ',
      width: 120,
      type: 'number',
      editable: false
    },
    {
      field: 'volumeRemainder',
      headerName: 'V³ остаток',
      width: 120,
      type: 'number',
      editable: false,
      valueGetter: (params: GridValueGetterParams) => 
        calculateRemainder(params.row.volumePlan, params.row.volumeFact)
    },
    {
      field: 'progress',
      headerName: 'Выполнение',
      width: 150,
      renderCell: (params: GridRenderCellParams) => (
        <Box sx={{ width: '100%', display: 'flex', alignItems: 'center' }}>
          <LinearProgress 
            variant="determinate" 
            value={params.row.progress} 
            sx={{ width: '80%' }} 
          />
          <Typography variant="body2" sx={{ ml: 1 }}>
            {params.row.progress}%
          </Typography>
        </Box>
      )
    },
    ...generateDailyColumns()
  ];

  const handleFieldChange = (id: string, field: keyof GPRRecordType, value: any) => {
    setRecords(prevRecords =>
      prevRecords.map(record => {
        if (record.id === id) {
          const updatedRecord = { ...record, [field]: value };
          
          // Если изменяем объем плана, пересчитываем остаток и прогресс
          if (field === 'volumePlan') {
            updatedRecord.volumeRemainder = calculateRemainder(value, record.volumeFact);
            updatedRecord.progress = calculateProgress(value, record.volumeFact);
          }
          
          return updatedRecord;
        }
        return record;
      })
    );
  };

  // Обновление еженедельного отчета
  const updateWeeklyReport = () => {
    if (!selectedWeekStart) return;
    
    // Здесь будет логика для вычисления недельного отчета
    // на основе выбранных дат и данных из records
    const report = workTypes.map(workType => {
      // Логика для суммирования плана и факта на неделе
      const planForWeek = records
        .filter(r => r.workType === workType.id)
        .reduce((sum, r) => sum + r.volumePlan, 0);
      
      const factForWeek = records
        .filter(r => r.workType === workType.id)
        .reduce((sum, r) => sum + r.volumeFact, 0);
      
      return {
        material: workType.name,
        plan: planForWeek,
        fact: factForWeek
      };
    });
    
    setWeeklyReport(report);
  };

  useEffect(() => {
    updateWeeklyReport();
  }, [records, selectedWeekStart]);

  return (
    <Box sx={{ height: 800, width: '100%', mt: 3 }}>
      <Paper elevation={3} sx={{ p: 2, mb: 3 }}>
        <Typography variant="h6" gutterBottom>
          График Производства Работ (ГПР)
        </Typography>
        
        <Box sx={{ mb: 2 }}>
          <TextField
            label="Начало недели для отчета"
            type="date"
            value={selectedWeekStart}
            onChange={(e) => setSelectedWeekStart(e.target.value)}
            InputLabelProps={{
              shrink: true,
            }}
            sx={{ mr: 2 }}
          />
        </Box>
        
        <DataGrid
          rows={records}
          columns={columns}
          editMode="cell"
          onCellEditCommit={(params: GridCellEditCommitParams) => {
            if (params.field === 'volumePlan' || params.field === 'customerId' || 
                params.field === 'objectId' || params.field === 'workType') {
              handleFieldChange(params.id as string, params.field as keyof GPRRecordType, params.value);
            }
          }}
          pageSize={10}
          rowsPerPageOptions={[10, 20, 50]}
        />
      </Paper>
      
      <Paper elevation={3} sx={{ p: 2 }}>
        <Typography variant="h6" gutterBottom>
          Недельный отчет
        </Typography>
        <DataGrid
          rows={weeklyReport}
          columns={[
            { field: 'material', headerName: 'Материал', width: 200 },
            { field: 'plan', headerName: 'План', width: 150, type: 'number' },
            { field: 'fact', headerName: 'Факт', width: 150, type: 'number' }
          ]}
          pageSize={10}
          rowsPerPageOptions={[10, 20, 50]}
          autoHeight
        />
      </Paper>
    </Box>
  );
};

export default GPRTable;