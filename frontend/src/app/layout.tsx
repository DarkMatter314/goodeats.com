import '@/styles/globals.css'
import { Inter } from 'next/font/google'
import { cn } from '@/lib/utils'
import Providers from '@/components/Providers'
import Navbar from '@/components/Navbar'

const inter = Inter({ subsets: ['latin'] })

export default function RootLayout({
  children,
}: {children: React.ReactNode}) {
  return (
    <html
    lang='en'
    className={cn('bg-white text-slate-900 antialiased', inter.className)}>
      <link rel='icon' href='/logo.png' />
      <body className='min-h-screen bg-slate-50 antialiased'>
        <Providers>
          <Navbar />
          <main>{children}</main>
        </Providers>
      </body>
    </html>
  )
}
