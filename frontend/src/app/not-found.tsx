import Icons from '@/components/Icons'
import { buttonVariants } from '@/ui/Button'
import LargeHeading from '@/ui/LargeHeading'
import Paragraph from '@/ui/Paragraph'
import Link from 'next/link'

import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Goodeats | Page not found',
  description: 'What would you like to cook today',
}

const PageNotFound: React.FC = () => {
  return (
    <section className='container pt-32 max-w-7xl mx-auto text-center flex flex-col gap-6 items-center'>
      <LargeHeading>Site not found...</LargeHeading>
      <Paragraph>The site you&apos;re searching for does not exist.</Paragraph>
      <Link href='/' className={buttonVariants({variant: 'default', className: 'w-fit'})}>
        <Icons.ChevronLeft className='mr-2 h-4 w-4' />
        Back to home
      </Link>
    </section>
  )
}

export default PageNotFound
