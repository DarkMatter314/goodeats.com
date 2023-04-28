import LargeHeading from '@/ui/LargeHeading'
import Paragraph from '@/ui/Paragraph'
import Link from 'next/link'
import Image from 'next/image'
import LoginForm from '@/components/LoginForm'
import { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Goodeats | Login',
  description: 'Login to your account',
}

const page: React.FC = () => {
  return (
    <div className='absolute pt-32 inset-0 mx-auto container flex h-screen flex-row items-center'>
      <div className='hidden lg:flex max-w-7xl w-1/2 h-full px-10'>
        <Image src='/food-1.jpg' alt='' width={1000} height={1000} className='w-full h-full object-contain' />
      </div>
      <div className='mx-auto max-w-7xl w-1/2 flex flex-col items-center space-y-6 px-10'>
        <div className='flex flex-col items-center gap-5 text-center'>
          <LargeHeading>Welcome back!</LargeHeading>
          <div className='flex flex-col items-center gap-2 text-center'>
            <LoginForm />
            <Paragraph size='sm'>
              Don&apos;t have an account? {' '}
              <Link href='/signup' className='underline underline-offset-2 font-medium text-black'>
                Sign Up
              </Link>
            </Paragraph>
          </div>
        </div>
      </div>
    </div>
  )
}

export default page
