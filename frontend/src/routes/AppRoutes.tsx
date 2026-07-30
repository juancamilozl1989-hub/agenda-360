import {
  BrowserRouter,
  Navigate,
  Route,
  Routes,
} from "react-router-dom";

import DashboardLayout from "../layouts/DashboardLayout";

import LoginPage from "../pages/Login/LoginPage";
import DashboardPage from "../pages/Dashboard/DashboardPage";
import AgendaPage from "../pages/Agenda/AgendaPage";

// Estas páginas las crearemos en el siguiente paso
import ClientesPage from "../pages/Clientes/ClientesPage.tsx";
import ServiciosPage from "../pages/Servicios/ServiciosPage.tsx";
import BarberosPage from "../pages/Barberos/BarberosPage.tsx";
import ReportesPage from "../pages/Reportes/ReportesPage.tsx";

export default function AppRoutes() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Login */}
        <Route
          path="/"
          element={<LoginPage />}
        />

        {/* Dashboard */}
        <Route
          path="/dashboard"
          element={
            <DashboardLayout>
              <DashboardPage />
            </DashboardLayout>
          }
        />

        {/* Agenda */}
        <Route
          path="/agenda"
          element={
            <DashboardLayout>
              <AgendaPage />
            </DashboardLayout>
          }
        />

        {/* Clientes */}
        <Route
          path="/clientes"
          element={
            <DashboardLayout>
              <ClientesPage />
            </DashboardLayout>
          }
        />

        {/* Servicios */}
        <Route
          path="/servicios"
          element={
            <DashboardLayout>
              <ServiciosPage />
            </DashboardLayout>
          }
        />

        {/* Barberos */}
        <Route
          path="/barberos"
          element={
            <DashboardLayout>
              <BarberosPage />
            </DashboardLayout>
          }
        />

        {/* Reportes */}
        <Route
          path="/reportes"
          element={
            <DashboardLayout>
              <ReportesPage />
            </DashboardLayout>
          }
        />

        {/* Redirección */}
        <Route
          path="*"
          element={<Navigate to="/" replace />}
        />
      </Routes>
    </BrowserRouter>
  );
}