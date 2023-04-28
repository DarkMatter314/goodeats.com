import * as jose from 'jose';
import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  const data = await request.json()
  const response = await fetch(`${process.env.BASE_API_URL}/register`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });
  const json = await response.json();
  if (!json.message) {
    return NextResponse.json(json);
  }
  const secret = new TextEncoder().encode(process.env.JWT_SECRET);
  const newJson = {
    user: data.username,
    user_id: json.user_id
  };
  const token = await new jose.SignJWT(newJson)
    .setExpirationTime('14d')
    .setProtectedHeader({ alg: 'HS256' })
    .sign(secret);
  return NextResponse.json({ token });
}
