'use client'

import { Icons } from '@/components/Icons'
import { Button } from '@/ui/Button'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuGroup,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/ui/DropdownMenu'
import Link from 'next/link'
import React from 'react'

export function RecipesMenu() {
  const [dropdownOpen, setDropdownOpen] = React.useState(false)
  const toggleDropdown = () => setDropdownOpen(!dropdownOpen)

  return (
    <DropdownMenu open={dropdownOpen} onOpenChange={setDropdownOpen}>
      <DropdownMenuTrigger asChild>
        <Button variant='link' className='center gap-2' onClick={toggleDropdown}>
          Recipes <Icons.ChevronDown size={16} />
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align='end' forceMount>
        <DropdownMenuGroup onClick={toggleDropdown}>
          <DropdownMenuItem>
            <Link href='/recipes' className='w-full'>
              All Recipes
            </Link>
          </DropdownMenuItem>
          <DropdownMenuItem>
            <Link href='/post-recipe' className='w-full'>
              Post a Recipe
            </Link>
          </DropdownMenuItem>
        </DropdownMenuGroup>
      </DropdownMenuContent>
    </DropdownMenu>
  )
}
