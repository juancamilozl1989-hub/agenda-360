import {
  Paper,
  Typography,
  Box,
  Tooltip,
} from "@mui/material";

export interface PuntoIngreso {
  etiqueta: string;
  valor: number;
}

interface RevenueChartProps {
  datos: PuntoIngreso[];
}

const moneda = (n: number) =>
  n.toLocaleString("es-CO", {
    style: "currency",
    currency: "COP",
    maximumFractionDigits: 0,
  });

export default function RevenueChart({ datos }: RevenueChartProps) {
  const maximo = Math.max(...datos.map((d) => d.valor), 0);

  return (
    <Paper
      sx={{
        p: 4,
        borderRadius: 4,
        bgcolor: "#1E1E1E",
        height: "100%",
      }}
    >
      <Typography variant="h6" fontWeight="bold" mb={1}>
        Ingresos de los últimos 7 días
      </Typography>

      <Typography variant="body2" color="gray" mb={3}>
        Calculados con las citas completadas.
      </Typography>

      {maximo === 0 ? (
        <Typography color="text.secondary" py={6} textAlign="center">
          Aún no hay citas completadas en este periodo.
        </Typography>
      ) : (
        <Box
          sx={{
            display: "flex",
            alignItems: "flex-end",
            justifyContent: "space-between",
            height: 220,
          }}
        >
          {datos.map((d) => (
            <Box
              key={d.etiqueta}
              sx={{
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                justifyContent: "flex-end",
                height: "100%",
              }}
            >
              <Tooltip title={moneda(d.valor)}>
                <Box
                  sx={{
                    width: 32,
                    height: `${(d.valor / maximo) * 85}%`,
                    minHeight: d.valor > 0 ? 6 : 2,
                    bgcolor: d.valor > 0 ? "#D4AF37" : "#333",
                    borderRadius: "8px 8px 0 0",
                    transition: ".3s",

                    "&:hover": {
                      bgcolor: "#E5C04A",
                    },
                  }}
                />
              </Tooltip>

              <Typography variant="caption" color="gray" mt={1}>
                {d.etiqueta}
              </Typography>
            </Box>
          ))}
        </Box>
      )}
    </Paper>
  );
}
