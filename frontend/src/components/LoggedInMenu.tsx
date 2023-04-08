import { Icons } from '@/components/Icons'
import { Button } from '@/components/ui/Button'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/DropdownMenu'
import Link from 'next/link'

export function LoggedInMenu() {
  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant='link' className='center'>
          username <Icons.ChevronDown size={16} />
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align='end' forceMount>
        <DropdownMenuItem>
          <Link href='/user' className='w-full'>My profile</Link>
        </DropdownMenuItem>
        <DropdownMenuItem>
          <Link href='/collections' className='w-full'>My Collections</Link>
        </DropdownMenuItem>
        <DropdownMenuItem>
          <Link href='/signout' className='w-full'>Sign Out</Link>
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  )
}

export default LoggedInMenu
