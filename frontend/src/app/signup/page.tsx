import LargeHeading from '@/ui/LargeHeading'
import Paragraph from '@/ui/Paragraph'
import Link from 'next/link'
import Image from 'next/image'
import SignupForm from '@/components/SignupForm'
import { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Goodeats | Sign Up',
}

const page: React.FC = () => {
  return (
    <div className='absolute inset-0 mx-auto container flex h-screen flex-row items-center justify-center'>
      <div className='hidden lg:flex max-w-7xl w-1/2 h-full px-10'>
        <Image src='/food-1.jpg' alt='' width={600} height={600} className='w-full h-full object-contain' />
      </div>
      <div className='mx-auto max-w-7xl w-1/2 flex flex-col items-center space-y-6 px-10'>
        <div className='flex flex-col items-center gap-5 text-center'>
          <LargeHeading>Welcome!</LargeHeading>
          <div className='flex flex-col items-center text-center'>
            <SignupForm />
            <Paragraph size='sm'>
              Have an account already? {' '}
              <Link href='/login' className='underline underline-offset-2 font-medium text-black'>
                Login
              </Link>
            </Paragraph>
          </div>
        </div>
      </div>
    </div>
  )
}

export default page
