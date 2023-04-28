'use client'

import React from 'react'
import Link from 'next/link'
import * as jose from 'jose';
import { useRouter } from 'next/navigation'
import { Button, buttonVariants, IconButton } from '@/ui/Button'
import { Icons } from '@/components/Icons'
import Drawer from '@mui/material/Drawer'
import { toast } from '@/ui/toast'

const MobileMenu = ({ secret }: { secret: string }) => {

  const [isDrawerOpen, setIsDrawerOpen] = React.useState(false)
  const [session, setSession] = React.useState(false);
  const [username, setUsername] = React.useState('');
  const router = useRouter();

  React.useEffect(() => {
    const fetchToken = async () => {
      // Check if there's a JWT token in localStorage
      const token = localStorage.getItem('token');
      if (token) {
        const secretKey = new TextEncoder().encode(secret);
        const { payload, protectedHeader } = await jose.jwtVerify(token, secretKey)
        if (payload) {
          const user = payload.user as string;
          setUsername(user);
          setSession(true);
        }
      } else {
        setSession(false);
      }
    }
    fetchToken();
    const intervalId = setInterval(fetchToken, 1000);
    return () => clearInterval(intervalId);
  }, [secret]);


  function toggleDrawer() {
    setIsDrawerOpen(!isDrawerOpen);
  }

  const signOut = () => {
    toast({
      title: 'Signing out...',
      message: '',
      type: 'default',
      duration: 1000,
    });
    localStorage.removeItem('token');
    setSession(false);
    setTimeout(() => {
      router.push('/');
    }, 1000);
  };

  return (
    <div className='flex flex-row md:hidden gap-4'>
      <IconButton icon={Icons.Search} variant='ghost' className='hover:bg-transparent' />
      <IconButton icon={Icons.Menu} variant='ghost' className='hover:bg-transparent focus:ring-0 focus:ring-offset-0' onClick={toggleDrawer} />
      <Drawer anchor='right' open={isDrawerOpen} onClose={toggleDrawer}>
        <div className='container h-full bg-orange-300/90 flex flex-col w-[180px] items-center pt-6'>
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
            {
              session ? (
                <>
                  <Link href={`/user/${username}`} className={buttonVariants({ variant: 'link' })} onClick={toggleDrawer}>
                    {username}&apos;s Profile
                  </Link>
                  <Link href='/collections' className={buttonVariants({ variant: 'link' })} onClick={toggleDrawer}>
                    My Collections
                  </Link>
                  <Button onClick={signOut} variant='link'>
                    Sign Out
                  </Button>
                </>
              ) : (
                <>
                  <Link
                    href='/login'
                    className={buttonVariants({ variant: 'link' })}>
                    Login
                  </Link>

                  <Link
                    href='/signup'
                    className={buttonVariants({ variant: 'default' })}>
                    Sign up
                  </Link>
                </>
              )
            }
          </div>
        </div>
      </Drawer>
    </div>
  )
}

export default MobileMenu
