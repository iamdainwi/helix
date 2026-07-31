import { NextRequest, NextResponse } from "next/server"
import axios from "axios"

const BACKEND = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000"

export async function GET(request: NextRequest) {
  try {
    const token = request.headers.get("authorization")
    const res = await axios.get(`${BACKEND}/users/me`, {
      headers: { Authorization: token ?? "" },
    })
    return NextResponse.json(res.data)
  } catch (error: any) {
    const status = error.response?.status || 500
    const data = error.response?.data || { detail: "Internal Server Error" }
    return NextResponse.json(data, { status })
  }
}

export async function PUT(request: NextRequest) {
  try {
    const body = await request.json()
    const token = request.headers.get("authorization")
    const res = await axios.put(`${BACKEND}/users/me`, body, {
      headers: { Authorization: token ?? "" },
    })
    return NextResponse.json(res.data)
  } catch (error: any) {
    const status = error.response?.status || 500
    const data = error.response?.data || { detail: "Internal Server Error" }
    return NextResponse.json(data, { status })
  }
}
