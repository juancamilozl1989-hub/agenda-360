import {
  Paper,
  Typography,
  Box,
} from "@mui/material";

const values = [45, 70, 55, 90, 60, 85, 75];

export default function RevenueChart() {
  return (
    <Paper
      sx={{
        p: 4,
        borderRadius: 4,
        bgcolor: "#1E1E1E",
        height: "100%",
      }}
    >
      <Typography
        variant="h6"
        fontWeight="bold"
        mb={3}
      >
        Ingresos de la semana
      </Typography>

      <Box
        sx={{
          display: "flex",
          alignItems: "flex-end",
          justifyContent: "space-between",
          height: 220,
        }}
      >
        {values.map((value, index) => (
          <Box
            key={index}
            sx={{
              width: 32,
              height: `${value}%`,
              bgcolor: "#D4AF37",
              borderRadius: "8px 8px 0 0",
              transition: ".3s",

              "&:hover": {
                bgcolor: "#E5C04A",
              },
            }}
          />
        ))}
      </Box>
    </Paper>
  );
}