import React from 'react';
import { Box, Typography, Tabs, Tab } from '@mui/material';
import GPRTable from '../components/Pto/GPRTable';

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

  const handleChange = (event: React.SyntheticEvent, newValue: number) => {
    setValue(newValue);
  };

  return (
    <Box sx={{ flexGrow: 1, bgcolor: 'background.paper', display: 'flex', mt: 3 }}>
      <Tabs
        orientation="vertical"
        variant="scrollable"
        value={value}
        onChange={handleChange}
        aria-label="Pto sections tabs"
        sx={{ borderRight: 1, borderColor: 'divider', minWidth: 200 }}
      >
        <Tab label="Раздел №1 - Список проектов" {...a11yProps(0)} />
        <Tab label="Раздел №2 - Исполнительная документация" {...a11yProps(1)} />
        <Tab label="Раздел №3 - Фактическое выполнение" {...a11yProps(2)} />
        <Tab label="Раздел №4 - Дорожные знаки" {...a11yProps(3)} />
        <Tab label="Раздел №5 - Справочник данных" {...a11yProps(4)} />
        <Tab label="Раздел №6 - Справочник материалов" {...a11yProps(5)} />
        <Tab label="Раздел №7 - Контроль" {...a11yProps(6)} />
        <Tab label="ГПР - График Производства Работ" {...a11yProps(7)} />
      </Tabs>
      <TabPanel value={value} index={0}>
        <Typography>Раздел №1 - Список проектов</Typography>
        <Typography>Здесь будет отображаться список всех проектов</Typography>
      </TabPanel>
      <TabPanel value={value} index={1}>
        <Typography>Раздел №2 - Исполнительная документация</Typography>
        <Typography>Здесь будет отображаться исполнительная документация</Typography>
      </TabPanel>
      <TabPanel value={value} index={2}>
        <Typography>Раздел №3 - Фактическое выполнение</Typography>
        <Typography>Здесь будет отображаться информация о фактическом выполнении работ</Typography>
      </TabPanel>
      <TabPanel value={value} index={3}>
        <Typography>Раздел №4 - Дорожные знаки</Typography>
        <Typography>Здесь будет отображаться информация о дорожных знаках</Typography>
      </TabPanel>
      <TabPanel value={value} index={4}>
        <Typography>Раздел №5 - Справочник данных</Typography>
        <Typography>Здесь будет отображаться справочник данных по ширинам линий и расчетам по ГОСТ</Typography>
      </TabPanel>
      <TabPanel value={value} index={5}>
        <Typography>Раздел №6 - Справочник материалов</Typography>
        <Typography>Здесь будет отображаться информация о материалах на складе</Typography>
      </TabPanel>
      <TabPanel value={value} index={6}>
        <Typography>Раздел №7 - Контроль</Typography>
        <Typography>Здесь будет отображаться информация о контроле материалов</Typography>
      </TabPanel>
      <TabPanel value={value} index={7}>
        <GPRTable />
      </TabPanel>
    </Box>
  );
};

export default PtoPage;