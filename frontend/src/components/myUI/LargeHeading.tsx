import { HTMLAttributes, forwardRef } from 'react';
import { VariantProps, cva } from 'class-variance-authority';
import { cn } from '@/lib/utils';

interface LargeHeadingProps {}

const LargeHeadingVariants = cva(
  'text-black text-center font-extrabold leading-tight tracking-tighter',
  {
    variants: {
      size: {
        default: 'text-4xl md:text-5xl lg:text-6xl',
        lg: 'text-5xl md:text-6xl lg:text-7xl',
        sm: 'text-2xl md:text-3xl lg:text-4xl',
        xs: 'text-xl md:text-2xl lg:text-3xl',
        xxs: 'text-lg md:text-xl lg:text-2xl',
        xxxs: 'text-base md:text-lg lg:text-xl',
        bottom: 'xs:text-lg sm:text-2xl md:text-3xl lg:text-4xl',
      },
    },
    defaultVariants: {
      size: 'default',
    }
  }
)

interface LargeHeadingProps
  extends HTMLAttributes<HTMLHeadingElement>,
    VariantProps<typeof LargeHeadingVariants> {}

const LargeHeading = forwardRef<HTMLHeadingElement, LargeHeadingProps>(({
    className, size, children, ...props
  }, ref) => {
      return (
        <p
          ref={ref}
          {...props}
          className={cn(LargeHeadingVariants({ size, className}))}>
          {children}
        </p>
      )
    }
  )

LargeHeading.displayName = 'LargeHeading'

export default LargeHeading
