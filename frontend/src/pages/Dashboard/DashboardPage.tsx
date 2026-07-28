import {
  Box,
  Grid,
  Typography,
} from "@mui/material";

import EventAvailableIcon from "@mui/icons-material/EventAvailable";
import GroupsIcon from "@mui/icons-material/Groups";
import ContentCutIcon from "@mui/icons-material/ContentCut";
import PaidIcon from "@mui/icons-material/Paid";

import StatCard from "../../components/cards/StatCard";
import RevenueChart from "../../components/dashboard/RevenueChart";
import RecentAppointments from "../../components/dashboard/RecentAppointments";
import TopServices from "../../components/dashboard/TopServices";
import TopBarbers from "../../components/dashboard/TopBarbers";

export default function DashboardPage() {
  return (
    <Box>
      {/* Encabezado */}
      <Typography
        variant="h4"
        fontWeight="bold"
      >
        Bienvenido, Camilo 👋
      </Typography>

      <Typography
        color="text.secondary"
        sx={{ mb: 4 }}
      >
        Aquí tienes un resumen de tu barbería para hoy.
      </Typography>

      {/* Tarjetas */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid size={{ xs: 12, md: 6, lg: 3 }}>
          <StatCard
            title="Citas Hoy"
            value="24"
            icon={<EventAvailableIcon />}
            color="#D4AF37"
          />
        </Grid>

        <Grid size={{ xs: 12, md: 6, lg: 3 }}>
          <StatCard
            title="Clientes"
            value="328"
            icon={<GroupsIcon />}
            color="#3B82F6"
          />
        </Grid>

        <Grid size={{ xs: 12, md: 6, lg: 3 }}>
          <StatCard
            title="Servicios"
            value="12"
            icon={<ContentCutIcon />}
            color="#10B981"
          />
        </Grid>

        <Grid size={{ xs: 12, md: 6, lg: 3 }}>
          <StatCard
            title="Ingresos"
            value="$2.350.000"
            icon={<PaidIcon />}
            color="#EF4444"
          />
        </Grid>
      </Grid>

      {/* Contenido principal */}
      <Grid container spacing={3}>
        {/* Columna izquierda */}
        <Grid size={{ xs: 12, lg: 8 }}>
          <RevenueChart />

          <Box mt={3}>
            <TopServices />
          </Box>
        </Grid>

        {/* Columna derecha */}
        <Grid size={{ xs: 12, lg: 4 }}>
          <RecentAppointments />

          <Box mt={3}>
            <TopBarbers />
          </Box>
        </Grid>
      </Grid>
    </Box>
  );
}