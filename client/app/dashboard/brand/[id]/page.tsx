'use client';

import { BrandDNA, BrandDNACard } from '@/components/brand-dna-card';
import { useEffect, useState } from 'react'
import { useParams } from 'next/navigation'
import apiClient from '@/lib/axios';
import { toast } from 'sonner';

interface BrandRecord {
  id: number;
  user_id: number;
  url: string;
  dna: BrandDNA;
  created_at: string;
}

const BrandDNADetails = () => {
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

  if (loading) return <div>Loading...</div>;
  if (!brand) return <div>Brand not found</div>;

  return (
    <div className='flex flex-col items-center justify-center m-6'>
      <BrandDNACard id={brand.id} url={brand.url} dna={brand.dna} createdAt={brand.created_at} />
    </div>
  );
}

export default BrandDNADetails;