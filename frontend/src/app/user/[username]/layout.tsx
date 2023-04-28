import { Metadata } from 'next'

export function generateMetadata({ params }): Metadata {
  return {
    title: `Goodeats | ${params.username}'s profile`,
  }
}

export default function RootLayout({children}: {children: React.ReactNode}) {
  return (
    <main>
      {children}
    </main>
  )
}
