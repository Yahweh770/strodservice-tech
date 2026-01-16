import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { AppBar, Toolbar, Typography, Drawer, List, ListItem, ListItemText, Box, ListItemIcon } from '@mui/material';
import { Description as DescriptionIcon, Dashboard as DashboardIcon } from '@mui/icons-material';
import './App.css';
import PtoPage from './pages/PtoPage';
import DocumentsPage from './pages/DocumentsPage';

function App() {
  const drawerWidth = 280;

  return (
    <Router>
      <Box sx={{ display: 'flex' }}>
        <AppBar position="fixed" sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}>
          <Toolbar>
            <Typography variant="h6" noWrap component="div">
              Строд-Сервис Технолоджи
            </Typography>
          </Toolbar>
        </AppBar>

        <Drawer
          variant="permanent"
          sx={{
            width: drawerWidth,
            flexShrink: 0,
            [`& .MuiDrawer-paper`]: { width: drawerWidth, boxSizing: 'border-box' },
          }}
        >
          <Toolbar />
          <List>
            <ListItem button component={Link} to="/">
              <ListItemIcon>
                <DashboardIcon />
              </ListItemIcon>
              <ListItemText primary="Главная" />
            </ListItem>
            <ListItem button component={Link} to="/pto">
              <ListItemIcon>
                <DashboardIcon />
              </ListItemIcon>
              <ListItemText primary="ПТО (Производство работ)" />
            </ListItem>
            <ListItem button component={Link} to="/documents">
              <ListItemIcon>
                <DescriptionIcon />
              </ListItemIcon>
              <ListItemText primary="Учет исполнительной документации" />
            </ListItem>
          </List>
        </Drawer>

        <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
          <Toolbar />
          <Routes>
            <Route path="/" element={
              <Box sx={{ textAlign: 'center', mt: 5 }}>
                <Typography variant="h4" gutterBottom>
                  Добро пожаловать в Строд-Сервис Технолоджи
                </Typography>
                <Typography variant="h6">
                  Выберите раздел в меню слева для начала работы
                </Typography>
                <Box sx={{ mt: 4, display: 'flex', justifyContent: 'center', gap: 4 }}>
                  <Box sx={{ textAlign: 'center' }}>
                    <DashboardIcon sx={{ fontSize: 60, color: 'primary.main' }} />
                    <Typography variant="h6" sx={{ mt: 1 }}>График Производства Работ</Typography>
                    <Typography variant="body2" color="text.secondary">Планирование и контроль выполнения работ</Typography>
                  </Box>
                  <Box sx={{ textAlign: 'center' }}>
                    <DescriptionIcon sx={{ fontSize: 60, color: 'secondary.main' }} />
                    <Typography variant="h6" sx={{ mt: 1 }}>Документооборот</Typography>
                    <Typography variant="body2" color="text.secondary">Учет и отслеживание документов</Typography>
                  </Box>
                </Box>
              </Box>
            } />
            <Route path="/pto" element={<PtoPage />} />
            <Route path="/documents" element={<DocumentsPage />} />
          </Routes>
        </Box>
      </Box>
    </Router>
  );
}

export default App;