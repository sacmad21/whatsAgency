/*
  Warnings:

  - You are about to drop the column `phoneNumberId` on the `Media` table. All the data in the column will be lost.

*/
-- DropForeignKey
ALTER TABLE `Media` DROP FOREIGN KEY `Media_phoneNumberId_fkey`;

-- DropIndex
DROP INDEX `Media_phoneNumberId_fkey` ON `Media`;

-- AlterTable
ALTER TABLE `Media` DROP COLUMN `phoneNumberId`;
