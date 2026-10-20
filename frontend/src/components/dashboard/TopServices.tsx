import {
  Paper,
  Typography,
  Box,
  LinearProgress,
} from "@mui/material";

export interface ServicioDestacado {
  name: string;
  count: number;
}

interface TopServicesProps {
  services: ServicioDestacado[];
}

export default function TopServices({ services }: TopServicesProps) {
  const maximo = Math.max(...services.map((s) => s.count), 1);

  return (
    <Paper
      sx={{
        p: 4,
        borderRadius: 4,
        bgcolor: "#1E1E1E",
      }}
    >
      <Typography variant="h6" fontWeight="bold" mb={3}>
        Servicios más solicitados
      </Typography>

      {services.length === 0 && (
        <Typography color="text.secondary">
          Todavía no hay citas para calcular los servicios más solicitados.
        </Typography>
      )}

      {services.map((service) => (
        <Box key={service.name} mb={3}>
          <Box display="flex" justifyContent="space-between" mb={1}>
            <Typography>{service.name}</Typography>

            <Typography color="#D4AF37" fontWeight="bold">
              {service.count}
            </Typography>
          </Box>

          <LinearProgress
            variant="determinate"
            value={(service.count / maximo) * 100}
            sx={{
              height: 10,
              borderRadius: 5,
              bgcolor: "#333",

              "& .MuiLinearProgress-bar": {
                bgcolor: "#D4AF37",
              },
            }}
          />
        </Box>
      ))}
    </Paper>
  );
}
