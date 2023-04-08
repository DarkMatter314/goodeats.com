'use client'

import * as React from 'react'
import Link from 'next/link'
import { buttonVariants, IconButton } from '@/ui/Button'
import { Icons } from '@/components/Icons'
import Drawer from '@mui/material/Drawer'
import { cn } from '@/lib/utils'

const MobileMenu = () => {
  // const session = await getServerSession()

  const [isDrawerOpen, setIsDrawerOpen] = React.useState(false)

  function toggleDrawer() {
    setIsDrawerOpen(!isDrawerOpen);
  }

  return (
    <div className='flex flex-row md:hidden gap-4'>
      <IconButton icon={Icons.Search} variant='ghost' className='hover:bg-transparent' />
      <IconButton icon={Icons.Menu} variant='ghost' className='hover:bg-transparent focus:ring-0 focus:ring-offset-0' onClick={toggleDrawer} />
      <Drawer anchor='right' open={isDrawerOpen} onClose={toggleDrawer}>
        <div className='container h-full bg-orange-300 flex flex-col w-[180px] items-center pt-6'>
          <div className='flex flex-col w-4/5 items-center gap-4'>
            <Link href='/about-us' className={buttonVariants({ variant: 'link' })} onClick={toggleDrawer}>
              About Us
            </Link>
            <Link href='/recipes' className={buttonVariants({ variant: 'link' })} onClick={toggleDrawer}>
              All Recipes
            </Link>
            <Link href='/post-recipe' className={buttonVariants({ variant: 'link' })} onClick={toggleDrawer}>
              Post a Recipe
            </Link>
            <Link href='/collections' className={buttonVariants({ variant: 'link' })} onClick={toggleDrawer}>
              Collections
            </Link>
            <Link href='/login' className={buttonVariants({ variant: 'link' })} onClick={toggleDrawer}>
              Login
            </Link>
            <Link href='/signup' className={cn(buttonVariants({ variant: 'outline' }), 'text-black border-black hover:text-slate-600 hover:border-slate-600')} onClick={toggleDrawer}>
              Sign up
            </Link>
          </div>
        </div>
      </Drawer>
    </div>
  )
}

export default MobileMenu
