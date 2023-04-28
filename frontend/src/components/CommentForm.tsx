'use client'

import * as Form from '@radix-ui/react-form';
import * as jose from 'jose';
import { Button } from '@/ui/Button';
import Icons from '@/components/Icons';
import { useState } from 'react';
import { toast } from '@/ui/toast';

interface CommentProps {
  id: string;
}

const CommentForm : React.FC<CommentProps> = ({id}: CommentProps) => {
  const [rating, setRating] = useState(0);
  const [reviewText, setReviewText] = useState('');

  const handleRatingChange = (value: number) => {
    setRating(value);
  }

  async function submitForm(data) {
    data = {
      rating: rating,
      review_text: reviewText,
    }
    const token = localStorage.getItem('token');
    if (!token) {
      toast({
        title: 'Error',
        message: 'Please login to add a review',
        type: 'error',
        duration: 2000,
      });
      return;
    }
    if (data.rating === 0) {
      toast({
        title: 'Error',
        message: 'Please select a rating',
        type: 'error',
        duration: 2000,
      });
      return;
    }
    // target api route
    const route_link = `/api/recipe/${id}/reviews/new`;

    // assign user_id
    data.user_id = jose.decodeJwt(token).user_id;

    const response = await fetch(route_link, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
    if (response.ok) {
      toast({
        title: 'Success',
        message: 'Your review has been added',
        type: 'success',
        duration: 2000,
      });
      setRating(0);
      setReviewText('');
    }
  };

  return (
    <Form.Root className='w-full flex flex-col items-center justify-center'
      onSubmit={(event) => {
        const data = Object.fromEntries(new FormData(event.currentTarget));
        submitForm(data);
        event.preventDefault();
      }}
    >
      <div className='w-full md:w-3/5 flex flex-col md:flex-row gap-5 justify-start items-end'>
        <div className='w-full flex flex-col gap-2 md:flex-row md:gap-5 items-start'>
          <Form.Field className='grid md:gap-[7px]' name='rating'>
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
                    className='h-6 w-6 cursor-pointer text-white'
                    fill={`${value <= rating ? 'white' : 'transparent'}`}
                    onClick={() => handleRatingChange(value)}
                  />
                ))}
              </div>
            </Form.Control>
          </Form.Field>
          <Form.Field className='w-full grid' name='comment'>
            <div className='flex items-baseline justify-between'>
              <Form.Label className='text-white font-medium text-[15px] leading-[35px]'>
                Comment (optional)
              </Form.Label>
            </div>
            <Form.Control asChild>
              <textarea
              value={reviewText}
              onChange={(e) => setReviewText(e.target.value)}
              className='pt-2 box-border w-full bg-blackA5 shadow-white inline-flex h-[60px] md:h-[35px] appearance-none items-center justify-center rounded-[4px] px-[10px] text-[15px] leading-none text-white shadow-[0_0_0_1px] outline-none hover:shadow-[0_0_0_1px] focus:shadow-[0_0_0_2px_white] selection:color-white' />
            </Form.Control>
          </Form.Field>
        </div>
        <div className='flex flex-col items-end'>
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
