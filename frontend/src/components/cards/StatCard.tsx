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
          px: 3,
        }}
      >
        <Box>
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

          <Typography
            variant="h4"
            sx={{
              mt: 1.5,
              fontWeight: 700,
            }}
          >
            {value}
          </Typography>
        </Box>

        <Box
          sx={{
            width: 68,
            height: 68,
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