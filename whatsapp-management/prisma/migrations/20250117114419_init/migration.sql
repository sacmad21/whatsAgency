/*
  Warnings:

  - Added the required column `address` to the `Contact` table without a default value. This is not possible if the table is not empty.
  - Added the required column `conversationType` to the `Contact` table without a default value. This is not possible if the table is not empty.
  - Added the required column `country` to the `Contact` table without a default value. This is not possible if the table is not empty.
  - Added the required column `email` to the `Contact` table without a default value. This is not possible if the table is not empty.
  - Added the required column `emailverfied` to the `Contact` table without a default value. This is not possible if the table is not empty.
  - Added the required column `facebookid` to the `Contact` table without a default value. This is not possible if the table is not empty.
  - Added the required column `facebookverified` to the `Contact` table without a default value. This is not possible if the table is not empty.
  - Added the required column `instaid` to the `Contact` table without a default value. This is not possible if the table is not empty.
  - Added the required column `instaidverified` to the `Contact` table without a default value. This is not possible if the table is not empty.
  - Added the required column `name` to the `Contact` table without a default value. This is not possible if the table is not empty.
  - Added the required column `phoneverified` to the `Contact` table without a default value. This is not possible if the table is not empty.
  - Added the required column `pincode` to the `Contact` table without a default value. This is not possible if the table is not empty.
  - Added the required column `xid` to the `Contact` table without a default value. This is not possible if the table is not empty.
  - Added the required column `xverified` to the `Contact` table without a default value. This is not possible if the table is not empty.

*/
-- AlterTable
ALTER TABLE `Contact` ADD COLUMN `address` VARCHAR(191) NOT NULL,
    ADD COLUMN `conversationType` VARCHAR(191) NOT NULL,
    ADD COLUMN `country` VARCHAR(191) NOT NULL,
    ADD COLUMN `email` VARCHAR(191) NOT NULL,
    ADD COLUMN `emailverfied` BOOLEAN NOT NULL,
    ADD COLUMN `facebookid` VARCHAR(191) NOT NULL,
    ADD COLUMN `facebookverified` BOOLEAN NOT NULL,
    ADD COLUMN `instaid` VARCHAR(191) NOT NULL,
    ADD COLUMN `instaidverified` BOOLEAN NOT NULL,
    ADD COLUMN `name` VARCHAR(191) NOT NULL,
    ADD COLUMN `phoneverified` BOOLEAN NOT NULL,
    ADD COLUMN `pincode` VARCHAR(191) NOT NULL,
    ADD COLUMN `xid` VARCHAR(191) NOT NULL,
    ADD COLUMN `xverified` BOOLEAN NOT NULL;
