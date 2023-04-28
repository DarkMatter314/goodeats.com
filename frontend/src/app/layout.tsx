import '@/styles/globals.css'
import { Inter } from 'next/font/google'
import { cn } from '@/lib/utils'
import Providers from '@/components/Providers'
import Navbar from '@/components/Navbar'
import { Toaster } from '@/ui/toast'
import { Metadata } from 'next'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Goodeats',
  description: 'What would you like to cook today',
}

export default function RootLayout({
  children,
}: {children: React.ReactNode}) {
  return (
    <html
    lang='en'
    className={cn('bg-white text-slate-900 antialiased', inter.className)}>
      <link rel='icon' href='/logo.png' />
      <body className='min-h-screen bg-slate-50 antialiased overflow-y-auto'>
        <Providers>
          <Navbar />
          <Toaster position='bottom-right' />
          <main className='flex flex-col'>{children}
         </main>
        </Providers>

      </body>
    </html>
  )
}
