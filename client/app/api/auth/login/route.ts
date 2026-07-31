// app/api/auth/login/route.ts
// Next.js Route Handler — proxies POST /auth/login to FastAPI backend

import { NextRequest } from "next/server"
import axios from "axios"

const BACKEND = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000"

export async function POST(request: NextRequest) {
  const body = await request.json()
  try {
    const res = await axios.post(`${BACKEND}/auth/login`, body)
    return Response.json(res.data, { status: 200 })
  } catch (err: unknown) {
    if (axios.isAxiosError(err)) {
      return Response.json(
        err.response?.data ?? { detail: "Login failed" },
        { status: err.response?.status ?? 500 }
      )
    }
    return Response.json({ detail: "Internal error" }, { status: 500 })
  }
}
