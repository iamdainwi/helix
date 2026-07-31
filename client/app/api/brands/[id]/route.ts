import { NextRequest, NextResponse } from "next/server"
import axios from "axios"

export const dynamic = "force-dynamic"

const BACKEND = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000"

export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const { id } = await params
    const token = request.headers.get("authorization")
    const res = await axios.get(`${BACKEND}/brands/${id}`, {
      headers: { Authorization: token ?? "" },
    })
    return NextResponse.json(res.data)
  } catch (error: unknown) {
    if (axios.isAxiosError(error)) {
      const status = error.response?.status || 500
      const data = error.response?.data || { detail: "Internal Server Error" }
      return NextResponse.json(data, { status })
    }
    return NextResponse.json({ detail: "Internal Server Error" }, { status: 500 })
  }
}

export async function DELETE(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const { id } = await params
    const token = request.headers.get("authorization")
    const res = await axios.delete(`${BACKEND}/brands/${id}`, {
      headers: { Authorization: token ?? "" },
    })
    return NextResponse.json(res.data)
  } catch (error: unknown) {
    if (axios.isAxiosError(error)) {
      const status = error.response?.status || 500
      const data = error.response?.data || { detail: "Internal Server Error" }
      return NextResponse.json(data, { status })
    }
    return NextResponse.json({ detail: "Internal Server Error" }, { status: 500 })
  }
}
