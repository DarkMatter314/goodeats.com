import { cn } from '@/lib/utils'
import { cva, VariantProps } from 'class-variance-authority'
import { Loader2 } from 'lucide-react'
import * as React from 'react'

const buttonVariants = cva(
  'active:scale-95 inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-black disabled:opacity-50 disabled:pointer-events-none',
  {
    variants: {
      variant: {
        default:
          'bg-slate-900 text-white hover:bg-slate-800',
        destructive: 'text-white hover:bg-red-600',
        outline:
          'bg-transparent text-white border border-slate-200',
        subtle:
          'bg-slate-100 text-slate-900 hover:bg-slate-200',
        ghost:
          'bg-transparent hover:bg-slate-100 data-[state=open]:bg-transparent',
        link: 'bg-transparent underline-offset-4 hover:underline text-slate-900 hover:bg-transparent',
      },
      size: {
        default: 'h-10 py-2 px-4',
        sm: 'h-9 px-2 rounded-md',
        lg: 'h-11 px-8 rounded-md',
      },
    },
    defaultVariants: {
      variant: 'default',
      size: 'default',
    },
  }
)

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
  VariantProps<typeof buttonVariants> {
  isLoading?: boolean
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, children, variant, isLoading, size, ...props }, ref) => {
    return (
      <button
        className={cn(buttonVariants({ variant, size, className }))}
        ref={ref}
        disabled={isLoading}
        {...props}>
        {isLoading ? <Loader2 className='mr-2 h-4 w-4 animate-spin' /> : null}
        {children}
      </button>
    )
  }
)

const iconButtonVariants = cva(
  'active:scale-95 inline-flex items-center justify-center rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-slate-200 disabled:opacity-50 disabled:pointer-events-none',
  {
    variants: {
      variant: {
        default:
          'bg-slate-900 hover:bg-slate-800',
        destructive: 'hover:bg-red-600',
        outline:
          'bg-slate-900 hover:bg-slate-800 border border-slate-200',
        subtle:
          'bg-slate-100 hover:bg-slate-200',
        ghost:
          'bg-transparent hover:bg-slate-100 data-[state=open]:bg-transparent',
        link: 'bg-transparent underline-offset-4 hover:underline hover:bg-transparent',
      },
      size: {
        default: 'h-10 w-10',
        sm: 'h-8 w-8',
        lg: 'h-11 w-11',
      },
    },
    defaultVariants: {
      variant: 'default',
      size: 'default',
    },
  }
)

export interface IconButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
  VariantProps<typeof iconButtonVariants> {
  icon: React.FC<{ className?: string }>
  isLoading?: boolean
}

const IconButton = React.forwardRef<HTMLButtonElement, IconButtonProps>(
  ({ icon: Icon, className = '', variant, size, ...props }, ref) => {
    return (
      <button
        type="button"
        className={cn(iconButtonVariants({ variant, size, className }))}
        ref={ref}
        {...props}>
        <Icon className='scale-90 md:scale-100' aria-hidden='true' />
      </button>
    );
  }
)

Button.displayName = 'Button'

IconButton.displayName = 'IconButton'

export { Button, buttonVariants, IconButton, iconButtonVariants }
