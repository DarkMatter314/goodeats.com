'use client'

import * as Form from '@radix-ui/react-form';
import { Button } from '@/ui/Button';
import { useRouter } from 'next/navigation';
import { toast } from '@/ui/toast';


const LoginForm = () => {

  const router = useRouter();

  async function submitForm(data) {
    if (data.remember == 'on') {
      data.remember = true;
    } else {
      data.remember = false;
    }
    const response = await fetch('/api/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
    const json = await response.json();
    if (json.token) {
      toast({
        title: 'Success',
        message: 'You are now logged in',
        type: 'success',
        duration: 1500,
      })
      const token = json.token;
      localStorage.setItem('token', token);
      setTimeout(() => {
        router.push('/');
      }, 1000);
    }
    else {
      const error_msg = json.message || json.password || json.username;
      toast({
        title: 'Error',
        message: error_msg,
        type: 'error',
        duration: 1000,
      });
    }
  };

  return (
    <Form.Root className='w-[360px] items-center px-8 md:px-0 pb-8'
      onSubmit={(event) => {
        const data = Object.fromEntries(new FormData(event.currentTarget));
        submitForm(data);
        event.preventDefault();
      }}
    >
      <Form.Field className='grid mb-[10px]' name='username'>
        <div className='flex items-baseline justify-between'>
          <Form.Label className='text-black font-medium text-[15px] leading-[35px]'>
            Username
          </Form.Label>
          <Form.Message className='text-black text-[13px] opacity-80' match='valueMissing'>
            Please enter your username
          </Form.Message>
        </div>
        <Form.Control asChild>
          <input
          className='box-border w-full bg-blackA5 shadow-blackA9 inline-flex h-[35px] appearance-none items-center justify-center rounded-[4px] px-[10px] text-[15px] leading-none text-black shadow-[0_0_0_1px] outline-none hover:shadow-[0_0_0_1px_black] focus:shadow-[0_0_0_2px_black]'
          type='text'
          required />
        </Form.Control>
      </Form.Field>
      <Form.Field className='grid mb-[10px]' name='password'>
        <div className='flex items-baseline justify-between'>
          <Form.Label className='text-black font-medium text-[15px] leading-[35px]'>
            Password
          </Form.Label>
        </div>
        <Form.Control asChild>
          <input
          className='box-border w-full bg-blackA5 shadow-blackA9 inline-flex h-[35px] appearance-none items-center justify-center rounded-[4px] px-[10px] text-[15px] leading-none text-black shadow-[0_0_0_1px] outline-none hover:shadow-[0_0_0_1px_black] focus:shadow-[0_0_0_2px_black] selection:color-white'
          type='password'
          required />
        </Form.Control>
      </Form.Field>
      <Form.Field className='flex flex-row items-center gap-2 justify-start mb-[15px]' name='remember'>
        <Form.Control asChild>
          <input
          className='bg-gray-200 hover:bg-gray-300 cursor-pointer w-4 h-4 focus:outline-none rounded-lg'
          type='checkbox' />
        </Form.Control>
        <div className='flex items-baseline justify-between'>
          <Form.Label className='text-black font-medium text-[15px] leading-[35px]'>
            Remember Me
          </Form.Label>
        </div>
      </Form.Field>
      <Form.Submit asChild>
        <Button className='w-full'>
          Login
        </Button>
      </Form.Submit>
    </Form.Root>
  )
};

export default LoginForm
