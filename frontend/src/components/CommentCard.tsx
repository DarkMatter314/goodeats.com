'use client'

import Link from 'next/link';
import Paragraph from '@/ui/Paragraph';
import { Icons } from '@/components/Icons';
import { IconButton } from '@/ui/Button';

interface CommentCardProps {
  reviewId: number;
  author: string;
  message: string;
  rating: number;
}

export function CommentCard({reviewId, author, message, rating}: CommentCardProps) {
  const likeCount = 0;
  const isLiked = false;
  return (
    <div className='w-full md:w-3/5 flex flex-col items-center'>
      <div className='flex flex-col md:flex-row w-full max-w-7xl'>
        <div className='flex flex-col w-full'>
          <div className='flex flex-row justify-between items-center'>
            <Link href={`/user/${author}`} className='text-lg md:text-xl font-bold text-start text-white mb-0'>
              {author}
            </Link>
            <div className='flex flex-row gap-1 items-center'>
              <IconButton icon={Icons.Heart} className={`${isLiked ? 'text-yellow-400' : 'text-white'} bg-transparent`} />
              <Paragraph className='font-bold text-start text-white mb-0'>
                {likeCount}
              </Paragraph>
            </div>
          </div>
          {
            message && (
              <Paragraph size='sm' className='w-full max-w-full text-start text-white'>
                {message}
              </Paragraph>
            )
          }
        </div>
      </div>
    </div>
  )
}
