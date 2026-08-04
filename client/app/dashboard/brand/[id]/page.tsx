'use client';

import { BrandDNA, BrandDNACard } from '@/components/brand-dna-card';
import { useEffect, useState } from 'react'
import { useParams } from 'next/navigation'
import apiClient from '@/lib/axios';
import { toast } from 'sonner';
import { Skeleton } from '@/components/ui/skeleton';
import { Card, CardContent, CardHeader } from '@/components/ui/card';
import { Separator } from '@/components/ui/separator';

interface BrandRecord {
  id: string;
  user_id: string;
  url: string;
  dna: BrandDNA;
  created_at: string;
}

export default function BrandDNADetails() {
  const [brand, setBrand] = useState<BrandRecord | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const { id } = useParams();

  useEffect(() => {
    if (!id) return;
    // setLoading(true);
    apiClient.get(`/api/brands/${id}`)
      .then(res => setBrand(res.data))
      .catch(() => toast.error('Could not load brand details'))
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) return (
    <div className='flex flex-col items-center justify-center m-6'>
      <Card className="w-full max-w-5xl rounded-3xl border-border/40 bg-card/40 backdrop-blur-md shadow-2xl">
        <CardHeader className="gap-2 p-8 md:p-10 pb-6 flex-row justify-between items-start">
          <div className="flex flex-col gap-3 flex-1">
            <Skeleton className="h-10 w-1/3" />
            <Skeleton className="h-4 w-1/4" />
            <Skeleton className="h-4 w-1/5" />
          </div>
          <Skeleton className="h-10 w-32" />
        </CardHeader>
        <Separator className="bg-border/30" />
        <CardContent className="p-8 md:p-10 grid gap-12 md:grid-cols-2 lg:grid-cols-3">
          <div className="flex flex-col gap-3">
            <Skeleton className="h-3 w-20" />
            <Skeleton className="h-6 w-3/4" />
          </div>
          <div className="flex flex-col gap-3">
            <Skeleton className="h-3 w-24" />
            <Skeleton className="h-6 w-full" />
            <Skeleton className="h-6 w-4/5" />
          </div>
          <div className="flex flex-col gap-3">
            <Skeleton className="h-3 w-24" />
            <div className="flex gap-2">
              <Skeleton className="h-6 w-16" />
              <Skeleton className="h-6 w-20" />
            </div>
          </div>
          <div className="flex flex-col gap-3">
            <Skeleton className="h-3 w-20" />
            <div className="flex gap-3">
              <Skeleton className="h-8 w-8 rounded-full" />
              <Skeleton className="h-8 w-8 rounded-full" />
              <Skeleton className="h-8 w-8 rounded-full" />
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
  if (!brand) return <div className="p-8 text-center text-muted-foreground">Brand not found</div>;

  return (
    <div className='flex flex-col items-center justify-center m-6'>
      <BrandDNACard id={brand.id} url={brand.url} dna={brand.dna} createdAt={brand.created_at} />
    </div>
  );
}