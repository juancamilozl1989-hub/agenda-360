import { useEffect, useMemo, useState } from "react";

import {
  Alert,
  Box,
  CircularProgress,
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

import { listarCitas } from "../../api/citasService";
import { listarClientes } from "../../api/clientesService";
import { listarServicios } from "../../api/serviciosService";
import { mensajeError } from "../../api/errores";
import type { Cita, Cliente, Servicio } from "../../api/tipos";
import { useAuth } from "../../context/AuthContext";
import {
  DIAS_CORTOS,
  desdeTexto,
  hoyTexto,
  mismoMes,
  sumarDias,
} from "../../utils/fechas";

const moneda = (n: number) =>
  n.toLocaleString("es-CO", {
    style: "currency",
    currency: "COP",
    maximumFractionDigits: 0,
  });

export default function DashboardPage() {
  const { userEmail } = useAuth();

  const [citas, setCitas] = useState<Cita[]>([]);
  const [clientes, setClientes] = useState<Cliente[]>([]);
  const [servicios, setServicios] = useState<Servicio[]>([]);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const cargar = async () => {
      try {
        const [c, cl, s] = await Promise.all([
          listarCitas(),
          listarClientes(),
          listarServicios(),
        ]);
        setCitas(c);
        setClientes(cl);
        setServicios(s);
      } catch (e) {
        setError(mensajeError(e, "No se pudo cargar el panel."));
      } finally {
        setCargando(false);
      }
    };

    cargar();
  }, []);

  // Todas las métricas se calculan a partir de los datos reales de la API
  const metricas = useMemo(() => {
    const hoy = hoyTexto();

    const citasHoy = citas.filter(
      (c) => c.fecha === hoy && c.estado !== "Cancelada"
    );

    const completadas = citas.filter((c) => c.estado === "Completada");

    const ingresosMes = completadas
      .filter((c) => mismoMes(c.fecha, hoy))
      .reduce((total, c) => total + c.service.precio, 0);

    // Ingresos por día de los últimos 7 días
    const ingresosSemana = Array.from({ length: 7 }, (_, i) => {
      const fecha = sumarDias(hoy, i - 6);
      const dia = (desdeTexto(fecha).getDay() + 6) % 7;

      return {
        etiqueta: DIAS_CORTOS[dia],
        valor: completadas
          .filter((c) => c.fecha === fecha)
          .reduce((t, c) => t + c.service.precio, 0),
      };
    });

    // Citas agrupadas por barbero y por servicio (sin contar canceladas)
    const vigentes = citas.filter((c) => c.estado !== "Cancelada");

    const contar = (claves: string[]) => {
      const conteo = new Map<string, number>();
      claves.forEach((k) => conteo.set(k, (conteo.get(k) ?? 0) + 1));
      return [...conteo.entries()]
        .sort((a, b) => b[1] - a[1])
        .slice(0, 3);
    };

    const topBarberos = contar(vigentes.map((c) => c.barber.nombre)).map(
      ([name, appointments]) => ({ name, appointments })
    );

    const topServicios = contar(vigentes.map((c) => c.service.nombre)).map(
      ([name, count]) => ({ name, count })
    );

    const proximasHoy = citasHoy
      .filter((c) => c.estado === "Pendiente" || c.estado === "Confirmada")
      .sort((a, b) => a.hora.localeCompare(b.hora))
      .slice(0, 5);

    return {
      citasHoy: citasHoy.length,
      ingresosMes,
      ingresosSemana,
      topBarberos,
      topServicios,
      proximasHoy,
    };
  }, [citas]);

  const serviciosActivos = servicios.filter(
    (s) => s.estado === "Activo"
  ).length;

  const nombre = userEmail ? userEmail.split("@")[0] : "";

  if (cargando) {
    return (
      <Box display="flex" justifyContent="center" py={10}>
        <CircularProgress sx={{ color: "#D4AF37" }} />
      </Box>
    );
  }

  return (
    <Box>
      {/* Encabezado */}
      <Typography variant="h4" fontWeight="bold">
        Bienvenido, {nombre} 👋
      </Typography>

      <Typography color="text.secondary" sx={{ mb: 4 }}>
        Aquí tienes un resumen de tu barbería para hoy.
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {/* Tarjetas */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid size={{ xs: 12, md: 6, lg: 3 }}>
          <StatCard
            title="Citas Hoy"
            value={String(metricas.citasHoy)}
            icon={<EventAvailableIcon />}
            color="#D4AF37"
          />
        </Grid>

        <Grid size={{ xs: 12, md: 6, lg: 3 }}>
          <StatCard
            title="Clientes"
            value={String(clientes.length)}
            icon={<GroupsIcon />}
            color="#3B82F6"
          />
        </Grid>

        <Grid size={{ xs: 12, md: 6, lg: 3 }}>
          <StatCard
            title="Servicios activos"
            value={String(serviciosActivos)}
            icon={<ContentCutIcon />}
            color="#10B981"
          />
        </Grid>

        <Grid size={{ xs: 12, md: 6, lg: 3 }}>
          <StatCard
            title="Ingresos del mes"
            value={moneda(metricas.ingresosMes)}
            icon={<PaidIcon />}
            color="#EF4444"
          />
        </Grid>
      </Grid>

      {/* Contenido principal */}
      <Grid container spacing={3}>
        {/* Columna izquierda */}
        <Grid size={{ xs: 12, lg: 8 }}>
          <RevenueChart datos={metricas.ingresosSemana} />

          <Box mt={3}>
            <TopServices services={metricas.topServicios} />
          </Box>
        </Grid>

        {/* Columna derecha */}
        <Grid size={{ xs: 12, lg: 4 }}>
          <RecentAppointments citas={metricas.proximasHoy} />

          <Box mt={3}>
            <TopBarbers barbers={metricas.topBarberos} />
          </Box>
        </Grid>
      </Grid>
    </Box>
  );
}
