import { Card, CardContent, Typography, Box } from "@mui/material";
import type { ReactNode } from "react";

interface StatCardProps {
  title: string;
  value: string;
  icon: ReactNode;
  color: string;
}

export default function StatCard({
  title,
  value,
  icon,
  color,
}: StatCardProps) {
  return (
    <Card
      elevation={0}
      sx={{
        height: 140,
        borderRadius: 5,
        bgcolor: "#1E1E1E",
        color: "#FFFFFF",
        border: "1px solid rgba(255,255,255,.08)",
        transition: "all .35s ease",
        cursor: "pointer",

        "&:hover": {
          transform: "translateY(-6px)",
          boxShadow: "0 20px 40px rgba(0,0,0,.45)",
          borderColor: "rgba(212,175,55,.35)",
        },
      }}
    >
      <CardContent
        sx={{
          height: "100%",
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          gap: 2,
          px: 3,
        }}
      >
        {/* minWidth: 0 permite que el texto se ajuste sin empujar el ícono */}
        <Box sx={{ minWidth: 0, flex: 1 }}>
          <Typography
            variant="body2"
            sx={{
              color: "#9E9E9E",
              fontWeight: 500,
              letterSpacing: 0.5,
            }}
          >
            {title}
          </Typography>

          {/* Hallazgo H-07: los montos largos (por ejemplo "$ 1.250.000")
              se montaban sobre el ícono. El tamaño de la fuente se reduce
              según la longitud del valor y nunca se parte en dos líneas. */}
          <Typography
            variant="h4"
            sx={{
              mt: 1.5,
              fontWeight: 700,
              whiteSpace: "nowrap",
              overflow: "hidden",
              textOverflow: "ellipsis",
              fontSize:
                value.length > 10
                  ? "1.1rem"
                  : value.length > 5
                    ? "1.35rem"
                    : undefined,
            }}
            title={value}
          >
            {value}
          </Typography>
        </Box>

        <Box
          sx={{
            width: 68,
            height: 68,
            flexShrink: 0,
            borderRadius: "50%",
            bgcolor: color,
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            color: "#FFF",
            fontSize: 32,
            boxShadow: `0 8px 20px ${color}55`,
            transition: ".3s",

            "& svg": {
              fontSize: 34,
            },
          }}
        >
          {icon}
        </Box>
      </CardContent>
    </Card>
  );
}