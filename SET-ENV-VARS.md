# 🔐 SET ENVIRONMENT VARIABLES DI VERCEL

## Cara Termudah: Via Vercel Dashboard

1. **Buka Project Settings**:
   https://vercel.com/dewas-projects-d0163f17/project-python/settings/environment-variables

2. **Tambahkan 3 Environment Variables berikut:**

### Variable 1: SUPABASE_URL

```
Name: SUPABASE_URL
Value: https://pislnvhdmsxudltcuuku.supabase.co
Environment: Production, Preview, Development (pilih semua)
```

### Variable 2: SUPABASE_ANON_KEY

```
Name: SUPABASE_ANON_KEY
Value: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBpc2xudmhkbXN4dWRsdGN1dWt1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjAzODI4MTYsImV4cCI6MjA3NTk1ODgxNn0.j-M6yrGTumWsJM8K5IX-RPpnMbCEvWqLxRiO9HMPq6A
Environment: Production, Preview, Development (pilih semua)
```

### Variable 3: SUPABASE_SERVICE_ROLE_KEY

```
Name: SUPABASE_SERVICE_ROLE_KEY
Value: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBpc2xudmhkbXN4dWRsdGN1dWt1Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MDM4MjgxNiwiZXhwIjoyMDc1OTU4ODE2fQ.hFIEd9nu_OSh0ar_vCYaCIs6CR_BmgPuB1Sx7NnsfWs
Environment: Production, Preview, Development (pilih semua)
```

3. **Save** setiap variable

4. **Redeploy**:

```bash
cd "/Users/dewasatriaaa/Downloads/KULIAH/PROJECT CODE/project python"
vercel --prod
```

---

## ✅ Setelah Set Environment Variables:

Redeploy project Anda dan test:

### 🔗 Production URL:

https://project-python-aybnima4a-dewas-projects-d0163f17.vercel.app

### 📄 Test Pages:

- Landing: https://project-python-aybnima4a-dewas-projects-d0163f17.vercel.app/
- Daftar: https://project-python-aybnima4a-dewas-projects-d0163f17.vercel.app/daftar
- Admin: https://project-python-aybnima4a-dewas-projects-d0163f17.vercel.app/admin

### 🔌 Test API:

- Create: https://project-python-aybnima4a-dewas-projects-d0163f17.vercel.app/api/pendaftar_create
- List: https://project-python-aybnima4a-dewas-projects-d0163f17.vercel.app/api/pendaftar_list

---

## 💡 Screenshot Langkah-langkah:

1. Buka link settings di atas
2. Klik "Add New" atau "Add Environment Variable"
3. Masukkan Name, Value, dan pilih Environment
4. Klik "Save"
5. Ulangi untuk 3 variables
6. Redeploy dengan `vercel --prod`

---

## 🎉 DONE!

Project Anda sudah live dan siap digunakan! 🚀
