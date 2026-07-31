// app/api/brands/generate/route.ts
// Next.js Route Handler — proxies POST /brands/generate to FastAPI backend

import { NextRequest } from "next/server"
import axios from "axios"

const BACKEND = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000"

export async function POST(request: NextRequest) {
  const body = await request.json()
  const token = request.headers.get("authorization")
  try {
    const res = await axios.post(`${BACKEND}/brands/generate`, body, {
      headers: { Authorization: token ?? "" },
    })
    return Response.json(res.data, { status: 200 })
  } catch (err: unknown) {
    if (axios.isAxiosError(err)) {
      return Response.json(
        err.response?.data ?? { detail: "Brand DNA generation failed" },
        { status: err.response?.status ?? 500 }
      )
    }
    return Response.json({ detail: "Internal error" }, { status: 500 })
  }
}
