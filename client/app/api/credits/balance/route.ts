// app/api/credits/balance/route.ts
// Next.js Route Handler — proxies GET /credits/balance to FastAPI backend

import { NextRequest } from "next/server"
import axios from "axios"

export const dynamic = "force-dynamic"

const BACKEND = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000"

export async function GET(request: NextRequest) {
  const token = request.headers.get("authorization")
  try {
    const res = await axios.get(`${BACKEND}/credits/balance`, {
      headers: { Authorization: token ?? "" },
    })
    return Response.json(res.data, { status: 200 })
  } catch (err: unknown) {
    if (axios.isAxiosError(err)) {
      return Response.json(
        err.response?.data ?? { detail: "Failed to fetch balance" },
        { status: err.response?.status ?? 500 }
      )
    }
    return Response.json({ detail: "Internal error" }, { status: 500 })
  }
}
