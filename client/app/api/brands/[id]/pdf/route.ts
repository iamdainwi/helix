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
    const res = await axios.get(`${BACKEND}/brands/${id}/pdf`, {
      headers: { Authorization: token ?? "" },
      responseType: "arraybuffer", // Important for binary data like PDF
    })
    
    return new NextResponse(res.data, {
      status: 200,
      headers: {
        "Content-Type": "application/pdf",
        "Content-Disposition": `attachment; filename="brand_dna_${id}.pdf"`,
      },
    })
  } catch (error: unknown) {
    if (axios.isAxiosError(error)) {
      const status = error.response?.status || 500
      const data = error.response?.data || { detail: "Internal Server Error" }
      return NextResponse.json(data, { status })
    }
    return NextResponse.json({ detail: "Internal Server Error" }, { status: 500 })
  }
}
