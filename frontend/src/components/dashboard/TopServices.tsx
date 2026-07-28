import {
  Paper,
  Typography,
  Box,
  LinearProgress,
} from "@mui/material";

const services = [
  { name: "Corte Clásico", value: 90 },
  { name: "Barba Premium", value: 72 },
  { name: "Corte + Barba", value: 55 },
];

export default function TopServices() {
  return (
    <Paper
      sx={{
        p: 4,
        borderRadius: 4,
        bgcolor: "#1E1E1E",
      }}
    >
      <Typography
        variant="h6"
        fontWeight="bold"
        mb={3}
      >
        Servicios más vendidos
      </Typography>

      {services.map((service) => (
        <Box key={service.name} mb={3}>
          <Typography mb={1}>
            {service.name}
          </Typography>

          <LinearProgress
            variant="determinate"
            value={service.value}
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