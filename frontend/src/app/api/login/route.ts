import * as jose from 'jose';
import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  const data = await request.json()
  let expiresIn = '1h'
  if (data.rememberMe) {
    expiresIn = '14d';
  }
  const response = await fetch(`${process.env.BASE_API_URL}/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });
  const json = await response.json();
  if (json?.user_id) {
    const secret = new TextEncoder().encode(process.env.JWT_SECRET);
    const newJson = {
      user: data.username,
      user_id: json.user_id
    };
    const token = await new jose.SignJWT(newJson)
      .setExpirationTime(expiresIn)
      .setProtectedHeader({ alg: 'HS256' })
      .sign(secret);
    return NextResponse.json({ token });
  }
  return NextResponse.json(json);
}
