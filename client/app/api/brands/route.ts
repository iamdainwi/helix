// app/api/brands/route.ts
// Next.js Route Handler — proxies GET /brands/ to FastAPI backend (list all brands)

import { NextRequest } from "next/server"
import axios from "axios"

export const dynamic = "force-dynamic"

const BACKEND = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000"

export async function GET(request: NextRequest) {
  const token = request.headers.get("authorization")
  try {
    const res = await axios.get(`${BACKEND}/brands/`, {
      headers: { Authorization: token ?? "" },
    })
    return Response.json(res.data, { status: 200 })
  } catch (err: unknown) {
    if (axios.isAxiosError(err)) {
      return Response.json(
        err.response?.data ?? { detail: "Failed to fetch brands" },
        { status: err.response?.status ?? 500 }
      )
    }
    return Response.json({ detail: "Internal error" }, { status: 500 })
  }
}
