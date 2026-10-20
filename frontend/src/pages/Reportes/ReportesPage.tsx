import { useEffect, useMemo, useState } from "react";

import {
  Alert,
  Box,
  Card,
  CardContent,
  CircularProgress,
  FormControl,
  Grid,
  InputLabel,
  MenuItem,
  Paper,
  Select,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography,
} from "@mui/material";

import PageHeader from "../../components/common/PageHeader";
import { listarCitas } from "../../api/citasService";
import { mensajeError } from "../../api/errores";
import type { Cita, EstadoCita } from "../../api/tipos";
import { hoyTexto, mismoMes } from "../../utils/fechas";

// ==========================================================
// Reportes de desempeño del negocio
// ==========================================================
// Igual que el dashboard, esta sección no tiene un endpoint
// propio: todas las cifras se calculan en el navegador a partir
// de las citas que entrega la API. Los ingresos solo suman las
// citas "Completada", para que una cita pendiente o cancelada
// no infle los resultados.

type Periodo = "mes" | "todo";

const ESTADOS: EstadoCita[] = [
  "Pendiente",
  "Confirmada",
  "Completada",
  "Cancelada",
];

const moneda = (n: number) =>
  n.toLocaleString("es-CO", {
    style: "currency",
    currency: "COP",
    maximumFractionDigits: 0,
  });

interface FilaDesempeno {
  nombre: string;
  citas: number;
  completadas: number;
  ingresos: number;
}

// Agrupa las citas por una clave (barbero o servicio) y calcula
// cuántas tiene, cuántas se completaron y cuánto dinero generaron.
function agrupar(citas: Cita[], clave: (c: Cita) => string): FilaDesempeno[] {
  const grupos = new Map<string, FilaDesempeno>();

  citas.forEach((c) => {
    const nombre = clave(c);
    const fila =
      grupos.get(nombre) ??
      { nombre, citas: 0, completadas: 0, ingresos: 0 };

    fila.citas += 1;

    if (c.estado === "Completada") {
      fila.completadas += 1;
      fila.ingresos += c.service.precio;
    }

    grupos.set(nombre, fila);
  });

  // Primero los que más ingresos generan; en empate, los que tienen más citas
  return [...grupos.values()].sort(
    (a, b) => b.ingresos - a.ingresos || b.citas - a.citas
  );
}

// Tarjeta pequeña de indicador
function Indicador({ titulo, valor }: { titulo: string; valor: string }) {
  return (
    <Card
      elevation={0}
      sx={{
        borderRadius: 5,
        bgcolor: "#1E1E1E",
        border: "1px solid rgba(255,255,255,.08)",
      }}
    >
      <CardContent sx={{ px: 3 }}>
        <Typography variant="body2" sx={{ color: "#9E9E9E" }}>
          {titulo}
        </Typography>
        <Typography
          variant="h5"
          sx={{ mt: 1, fontWeight: 700, color: "#D4AF37" }}
        >
          {valor}
        </Typography>
      </CardContent>
    </Card>
  );
}

// Tabla de desempeño (por barbero o por servicio)
function TablaDesempeno({
  titulo,
  columna,
  filas,
}: {
  titulo: string;
  columna: string;
  filas: FilaDesempeno[];
}) {
  return (
    <Box mb={4}>
      <Typography variant="h6" fontWeight="bold" mb={2}>
        {titulo}
      </Typography>

      <TableContainer component={Paper} sx={{ borderRadius: 4 }}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell><strong>{columna}</strong></TableCell>
              <TableCell><strong>Citas</strong></TableCell>
              <TableCell><strong>Completadas</strong></TableCell>
              <TableCell><strong>Ingresos</strong></TableCell>
            </TableRow>
          </TableHead>

          <TableBody>
            {filas.length === 0 ? (
              <TableRow>
                <TableCell colSpan={4} sx={{ color: "text.secondary" }}>
                  No hay citas en el periodo seleccionado.
                </TableCell>
              </TableRow>
            ) : (
              filas.map((f) => (
                <TableRow key={f.nombre} hover>
                  <TableCell>{f.nombre}</TableCell>
                  <TableCell>{f.citas}</TableCell>
                  <TableCell>{f.completadas}</TableCell>
                  <TableCell>{moneda(f.ingresos)}</TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
}

export default function ReportesPage() {
  const [citas, setCitas] = useState<Cita[]>([]);
  const [periodo, setPeriodo] = useState<Periodo>("mes");
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const cargar = async () => {
      try {
        setCitas(await listarCitas());
      } catch (e) {
        setError(mensajeError(e, "No se pudieron cargar los reportes."));
      } finally {
        setCargando(false);
      }
    };

    cargar();
  }, []);

  const reporte = useMemo(() => {
    const hoy = hoyTexto();

    // Citas del periodo elegido
    const delPeriodo =
      periodo === "mes"
        ? citas.filter((c) => mismoMes(c.fecha, hoy))
        : citas;

    const completadas = delPeriodo.filter((c) => c.estado === "Completada");
    const canceladas = delPeriodo.filter((c) => c.estado === "Cancelada");

    const ingresos = completadas.reduce((t, c) => t + c.service.precio, 0);

    // Ticket promedio: ingreso medio por cita completada
    const ticket = completadas.length ? ingresos / completadas.length : 0;

    // Porcentaje de citas canceladas sobre el total del periodo
    const tasaCancelacion = delPeriodo.length
      ? (canceladas.length / delPeriodo.length) * 100
      : 0;

    const porEstado = ESTADOS.map((estado) => ({
      estado,
      total: delPeriodo.filter((c) => c.estado === estado).length,
    }));

    return {
      total: delPeriodo.length,
      ingresos,
      ticket,
      tasaCancelacion,
      porEstado,
      porBarbero: agrupar(delPeriodo, (c) => c.barber.nombre),
      porServicio: agrupar(delPeriodo, (c) => c.service.nombre),
    };
  }, [citas, periodo]);

  if (cargando) {
    return (
      <Box display="flex" justifyContent="center" py={10}>
        <CircularProgress sx={{ color: "#D4AF37" }} />
      </Box>
    );
  }

  return (
    <Box>
      <PageHeader
        title="Reportes"
        subtitle="Desempeño del negocio calculado con las citas registradas."
      />

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {/* Selector de periodo */}
      <FormControl size="small" sx={{ minWidth: 200, mb: 3 }}>
        <InputLabel id="periodo-label">Periodo</InputLabel>
        <Select
          labelId="periodo-label"
          label="Periodo"
          value={periodo}
          onChange={(e) => setPeriodo(e.target.value as Periodo)}
        >
          <MenuItem value="mes">Mes actual</MenuItem>
          <MenuItem value="todo">Todo el historial</MenuItem>
        </Select>
      </FormControl>

      {/* Indicadores principales */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid size={{ xs: 12, sm: 6, lg: 3 }}>
          <Indicador titulo="Citas del periodo" valor={String(reporte.total)} />
        </Grid>
        <Grid size={{ xs: 12, sm: 6, lg: 3 }}>
          <Indicador titulo="Ingresos" valor={moneda(reporte.ingresos)} />
        </Grid>
        <Grid size={{ xs: 12, sm: 6, lg: 3 }}>
          <Indicador titulo="Ticket promedio" valor={moneda(reporte.ticket)} />
        </Grid>
        <Grid size={{ xs: 12, sm: 6, lg: 3 }}>
          <Indicador
            titulo="Cancelaciones"
            valor={`${reporte.tasaCancelacion.toFixed(1)} %`}
          />
        </Grid>
      </Grid>

      {/* Distribución por estado */}
      <Card
        elevation={0}
        sx={{
          borderRadius: 5,
          bgcolor: "#1E1E1E",
          border: "1px solid rgba(255,255,255,.08)",
          mb: 4,
        }}
      >
        <CardContent sx={{ px: 3 }}>
          <Typography variant="h6" fontWeight="bold" mb={2}>
            Citas por estado
          </Typography>

          <Box display="flex" flexWrap="wrap" gap={4}>
            {reporte.porEstado.map(({ estado, total }) => (
              <Box key={estado}>
                <Typography variant="h5" fontWeight={700}>
                  {total}
                </Typography>
                <Typography variant="body2" sx={{ color: "#9E9E9E" }}>
                  {estado}
                </Typography>
              </Box>
            ))}
          </Box>
        </CardContent>
      </Card>

      <TablaDesempeno
        titulo="Desempeño por barbero"
        columna="Barbero"
        filas={reporte.porBarbero}
      />

      <TablaDesempeno
        titulo="Desempeño por servicio"
        columna="Servicio"
        filas={reporte.porServicio}
      />
    </Box>
  );
}
