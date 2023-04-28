import { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Goodeats | Browse Recipes',
}

export default function RootLayout({children}: {children: React.ReactNode}) {
  return (
    <main>
      {children}
    </main>
  )
}
