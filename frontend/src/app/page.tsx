import { Inter } from 'next/font/google'
import { Metadata } from 'next'
import LargeHeading from '@/components/ui/LargeHeading'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Goodeats',
  description: 'What would you like to cook today',
}

export default function Home() {
  return (
    <div className='relative h-screen flex items-center justify-center overflow-x-hidden'>
      <div className='container pt-32 max-w-full w-full h-full mx-2 md:mx-5'>
        <div className='h-full gap-6 flex flex-col justify-start lg:justify-center items-center lg:items-start'>
          <LargeHeading size='lg' className='text-black'>
            Get some nice recipes
          </LargeHeading>
        </div>
      </div>
    </div>
  )
}
