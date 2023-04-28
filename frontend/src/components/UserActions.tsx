'use client'

import React from 'react'
import Link from 'next/link'
import * as jose from 'jose';
import { toast } from '@/ui/toast'
import { useRouter } from 'next/navigation'
import { buttonVariants } from '@/ui/Button'
import { Icons } from '@/components/Icons'
import { Button } from '@/ui/Button'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuGroup,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/ui/DropdownMenu'

const UserActions = ({ secret } : { secret: string }) => {
  const [session, setSession] = React.useState(false);
  const [username, setUsername] = React.useState('');
  const [dropdownOpen, setDropdownOpen] = React.useState(false)
  const toggleDropdown = () => setDropdownOpen(!dropdownOpen)
  const router = useRouter();

  React.useEffect(() => {
    const fetchToken = async () => {
      // Check if there's a JWT token in localStorage
      const token = localStorage.getItem('token');
      if (token) {
        const secretKey = new TextEncoder().encode(secret);
        try {
          const { payload, protectedHeader } = await jose.jwtVerify(token, secretKey)
          if (payload) {
            const user = payload.user as string;
            setUsername(user);
            setSession(true);
          }
        } catch (err) {
          localStorage.removeItem('token');
          setSession(false);
        }
      } else {
        setSession(false);
      }
    }
    fetchToken();
    const intervalId = setInterval(fetchToken, 1000);
    return () => clearInterval(intervalId);
  }, [secret]);

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

  return (session ? (
    <DropdownMenu open={dropdownOpen} onOpenChange={setDropdownOpen}>
      <DropdownMenuTrigger asChild>
        <Button variant='link' className='font-bold center gap-2' onClick={toggleDropdown}>
          {username} <Icons.ChevronDown size={16} strokeWidth={3} />
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align='end' forceMount>
        <DropdownMenuGroup onClick={toggleDropdown}>
          <DropdownMenuItem>
            <Link href={`/user/${username}`} className='w-full h-full'>
              My Profile
            </Link>
          </DropdownMenuItem>
          <DropdownMenuItem>
            <Link href='/collections' className='w-full'>
              My Collections
            </Link>
          </DropdownMenuItem>
          <DropdownMenuItem>
            <a onClick={signOut} className='w-full cursor-pointer'>
              Sign Out
            </a>
          </DropdownMenuItem>
        </DropdownMenuGroup>
      </DropdownMenuContent>
    </DropdownMenu>
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
  )
}

export default UserActions
