import React from 'react';
import { Box, Typography, Tabs, Tab } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import GPRTable from '../components/Pto/GPRTable';
import DocumentsPage from './DocumentsPage';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`vertical-tabpanel-${index}`}
      {...other}
    >
      {value === index && (
        <Box sx={{ p: 3 }}>
          <Typography>{children}</Typography>
        </Box>
      )}
    </div>
  );
}

function a11yProps(index: number) {
  return {
    id: `vertical-tab-${index}`,
    'aria-controls': `vertical-tabpanel-${index}`,
  };
}

const PtoPage: React.FC = () => {
  const [value, setValue] = React.useState(0);
  const navigate = useNavigate();

  const handleChange = (event: React.SyntheticEvent, newValue: number) => {
    setValue(newValue);
  };

  const handleDocumentSectionClick = () => {
    // Navigate to the documents page
    navigate('/documents');
  };

  return (
    <Box sx={{ flexGrow: 1, bgcolor: 'background.paper', display: 'flex', mt: 3 }}>
      <Tabs
        orientation="vertical"
        variant="scrollable"
        value={value}
        onChange={handleChange}
        aria-label="Pto sections tabs"
        sx={{ borderRight: 1, borderColor: 'divider', minWidth: 250 }}
      >
        <Tab label="Раздел №1 - Список проектов" {...a11yProps(0)} />
        <Tab 
          label="Раздел №2 - Исполнительная документация" 
          {...a11yProps(1)} 
          onClick={handleDocumentSectionClick}
        />
        <Tab label="Раздел №3 - Фактическое выполнение" {...a11yProps(2)} />
        <Tab label="Раздел №4 - Дорожные знаки" {...a11yProps(3)} />
        <Tab label="Раздел №5 - Справочник данных" {...a11yProps(4)} />
        <Tab label="Раздел №6 - Справочник материалов" {...a11yProps(5)} />
        <Tab label="Раздел №7 - Контроль" {...a11yProps(6)} />
        <Tab label="ГПР - График Производства Работ" {...a11yProps(7)} />
      </Tabs>
      <TabPanel value={value} index={0}>
        <Typography variant="h5" gutterBottom>
          Раздел №1 - Список проектов
        </Typography>
        <Typography>Здесь будет отображаться список всех проектов</Typography>
        <Typography paragraph sx={{ mt: 2 }}>
          В этом разделе вы можете просматривать, создавать и управлять проектами строительства.
          Каждый проект включает в себя информацию о заказчике, объекте, сроках выполнения и текущем статусе.
        </Typography>
      </TabPanel>
      <TabPanel value={value} index={1}>
        <Typography variant="h5" gutterBottom>
          Раздел №2 - Исполнительная документация
        </Typography>
        <Typography>Здесь будет отображаться исполнительная документация</Typography>
        <Typography paragraph sx={{ mt: 2 }}>
          Перейдите на страницу управления документами, чтобы добавлять, отправлять и возвращать документы.
          Система позволяет отслеживать статус каждого документа, историю отправок и возвратов.
        </Typography>
      </TabPanel>
      <TabPanel value={value} index={2}>
        <Typography variant="h5" gutterBottom>
          Раздел №3 - Фактическое выполнение
        </Typography>
        <Typography>Здесь будет отображаться информация о фактическом выполнении работ</Typography>
        <Typography paragraph sx={{ mt: 2 }}>
          В этом разделе отражается реальное состояние выполнения работ по сравнению с плановыми показателями.
          Вы можете вносить данные о выполненных объемах и анализировать отклонения от графика.
        </Typography>
      </TabPanel>
      <TabPanel value={value} index={3}>
        <Typography variant="h5" gutterBottom>
          Раздел №4 - Дорожные знаки
        </Typography>
        <Typography>Здесь будет отображаться информация о дорожных знаках</Typography>
        <Typography paragraph sx={{ mt: 2 }}>
          Справочник дорожных знаков с классификацией по типам, размерам и применению.
          Информация используется для планирования и выполнения работ по организации дорожного движения.
        </Typography>
      </TabPanel>
      <TabPanel value={value} index={4}>
        <Typography variant="h5" gutterBottom>
          Раздел №5 - Справочник данных
        </Typography>
        <Typography>Здесь будет отображаться справочник данных по ширинам линий и расчетам по ГОСТ</Typography>
        <Typography paragraph sx={{ mt: 2 }}>
          Стандартизированные данные по ширине линий разметки, требованиям ГОСТ и другим нормативам.
          Эти данные используются для расчетов и проектирования работ.
        </Typography>
      </TabPanel>
      <TabPanel value={value} index={5}>
        <Typography variant="h5" gutterBottom>
          Раздел №6 - Справочник материалов
        </Typography>
        <Typography>Здесь будет отображаться информация о материалах на складе</Typography>
        <Typography paragraph sx={{ mt: 2 }}>
          Полный перечень материалов с характеристиками, остатками на складе, потребностями по проектам.
          Система позволяет планировать закупки и отслеживать использование материалов.
        </Typography>
      </TabPanel>
      <TabPanel value={value} index={6}>
        <Typography variant="h5" gutterBottom>
          Раздел №7 - Контроль
        </Typography>
        <Typography>Здесь будет отображаться информация о контроле материалов</Typography>
        <Typography paragraph sx={{ mt: 2 }}>
          Инструменты для контроля качества материалов, проверок, актов приемки и отчетности.
          Все данные фиксируются с возможностью прикрепления фотографий и документов.
        </Typography>
      </TabPanel>
      <TabPanel value={value} index={7}>
        <GPRTable />
      </TabPanel>
    </Box>
  );
};

export default PtoPage;