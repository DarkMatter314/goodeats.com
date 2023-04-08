'use client'

import * as Form from '@radix-ui/react-form';
import { Button } from '@/ui/Button';
import Icons from '@/components/Icons';
import { useState } from 'react';

const CommentForm = () => {
  const [rating, setRating] = useState(0)

  const handleRatingChange = (value: number) => {
    setRating(value)
  }

  return (
  <Form.Root className='w-full flex flex-col items-center justify-center'>
    <div className='w-full md:w-2/5 px-8 flex flex-col items-center mr-0 md:mr-5'>
      <Form.Field className='w-full grid mb-[10px]' name='rating'>
        <div className='flex items-baseline justify-between'>
          <Form.Label className='text-white font-medium text-[15px] leading-[35px]'>
            Rate this recipe
          </Form.Label>
          <Form.Message className='text-white text-[13px] opacity-80' match='tooShort'>
            Please rate
          </Form.Message>
        </div>
        <Form.Control asChild>
          <div className='flex flex-row gap-1'>
            {[1, 2, 3, 4, 5].map((value) => (
              <Icons.Star
                key={value}
                className={`h-6 w-6 cursor-pointer ${
                  value <= rating ? 'text-yellow-500' : 'text-slate-100'
                }`}
                onClick={() => handleRatingChange(value)}
              />
            ))}
          </div>
        </Form.Control>
      </Form.Field>
      <Form.Field className='w-full grid mb-[10px]' name='comment'>
        <div className='flex items-baseline justify-between'>
          <Form.Label className='text-white font-medium text-[15px] leading-[35px]'>
            Comment (optional)
          </Form.Label>
        </div>
        <Form.Control asChild>
          <textarea className='pt-1 box-border w-full bg-blackA5 shadow-white inline-flex h-[80px] appearance-none items-center justify-center rounded-[4px] px-[10px] text-[15px] leading-none text-white shadow-[0_0_0_1px] outline-none hover:shadow-[0_0_0_1px] focus:shadow-[0_0_0_2px_white] selection:color-white' />
        </Form.Control>
      </Form.Field>
      <div className='w-full flex flex-col items-end'>
        <Form.Submit asChild>
          <Button className='bg-white text-black/100 hover:bg-slate-100'>
            Review
          </Button>
        </Form.Submit>
      </div>
    </div>
  </Form.Root>
)};

export default CommentForm
