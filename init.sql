USE [master]
GO
/****** Object:  Database [ALITAS EL COMELON SF]    Script Date: 2/2/2026 09:13:32 p. m. ******/
CREATE DATABASE [ALITAS EL COMELON SF]
 CONTAINMENT = NONE
 ON  PRIMARY 
( NAME = N'ALITAS EL COMELON SF', FILENAME = N'C:\Program Files\Microsoft SQL Server\MSSQL16.SQLEXPRESS\MSSQL\DATA\ALITAS EL COMELON SF.mdf' , SIZE = 73728KB , MAXSIZE = UNLIMITED, FILEGROWTH = 65536KB )
 LOG ON 
( NAME = N'ALITAS EL COMELON SF_log', FILENAME = N'C:\Program Files\Microsoft SQL Server\MSSQL16.SQLEXPRESS\MSSQL\DATA\ALITAS EL COMELON SF_log.ldf' , SIZE = 8192KB , MAXSIZE = 2048GB , FILEGROWTH = 65536KB )
 COLLATE Modern_Spanish_CI_AS
 WITH CATALOG_COLLATION = DATABASE_DEFAULT, LEDGER = OFF
GO
ALTER DATABASE [ALITAS EL COMELON SF] SET COMPATIBILITY_LEVEL = 160
GO
IF (1 = FULLTEXTSERVICEPROPERTY('IsFullTextInstalled'))
begin
EXEC [ALITAS EL COMELON SF].[dbo].[sp_fulltext_database] @action = 'enable'
end
GO
ALTER DATABASE [ALITAS EL COMELON SF] SET ANSI_NULL_DEFAULT OFF 
GO
ALTER DATABASE [ALITAS EL COMELON SF] SET ANSI_NULLS OFF 
GO
ALTER DATABASE [ALITAS EL COMELON SF] SET ANSI_PADDING OFF 
GO
ALTER DATABASE [ALITAS EL COMELON SF] SET ANSI_WARNINGS OFF 
GO
ALTER DATABASE [ALITAS EL COMELON SF] SET ARITHABORT OFF 
GO
ALTER DATABASE [ALITAS EL COMELON SF] SET AUTO_CLOSE OFF 
GO
ALTER DATABASE [ALITAS EL COMELON SF] SET AUTO_SHRINK OFF 
GO
ALTER DATABASE [ALITAS EL COMELON SF] SET AUTO_UPDATE_STATISTICS ON 
GO
ALTER DATABASE [ALITAS EL COMELON SF] SET CURSOR_CLOSE_ON_COMMIT OFF 
GO
ALTER DATABASE [ALITAS EL COMELON SF] SET CURSOR_DEFAULT  GLOBAL 
GO
ALTER DATABASE [ALITAS EL COMELON SF] SET CONCAT_NULL_YIELDS_NULL OFF 
GO
ALTER DATABASE [ALITAS EL COMELON SF] SET NUMERIC_ROUNDABORT OFF 
GO
ALTER DATABASE [ALITAS EL COMELON SF] SET QUOTED_IDENTIFIER OFF 
GO
ALTER DATABASE [ALITAS EL COMELON SF] SET RECURSIVE_TRIGGERS OFF 
GO
ALTER DATABASE [ALITAS EL COMELON SF] SET  DISABLE_BROKER 
GO
ALTER DATABASE [ALITAS EL COMELON SF] SET AUTO_UPDATE_STATISTICS_ASYNC OFF 
GO
ALTER DATABASE [ALITAS EL COMELON SF] SET DATE_CORRELATION_OPTIMIZATION OFF 
GO
ALTER DATABASE [ALITAS EL COMELON SF] SET TRUSTWORTHY OFF 
GO
ALTER DATABASE [ALITAS EL COMELON SF] SET ALLOW_SNAPSHOT_ISOLATION OFF 
GO
ALTER DATABASE [ALITAS EL COMELON SF] SET PARAMETERIZATION SIMPLE 
GO
ALTER DATABASE [ALITAS EL COMELON SF] SET READ_COMMITTED_SNAPSHOT OFF 
GO
ALTER DATABASE [ALITAS EL COMELON SF] SET HONOR_BROKER_PRIORITY OFF 
GO
ALTER DATABASE [ALITAS EL COMELON SF] SET RECOVERY SIMPLE 
GO
ALTER DATABASE [ALITAS EL COMELON SF] SET  MULTI_USER 
GO
ALTER DATABASE [ALITAS EL COMELON SF] SET PAGE_VERIFY CHECKSUM  
GO
ALTER DATABASE [ALITAS EL COMELON SF] SET DB_CHAINING OFF 
GO
ALTER DATABASE [ALITAS EL COMELON SF] SET FILESTREAM( NON_TRANSACTED_ACCESS = OFF ) 
GO
ALTER DATABASE [ALITAS EL COMELON SF] SET TARGET_RECOVERY_TIME = 60 SECONDS 
GO
ALTER DATABASE [ALITAS EL COMELON SF] SET DELAYED_DURABILITY = DISABLED 
GO
ALTER DATABASE [ALITAS EL COMELON SF] SET ACCELERATED_DATABASE_RECOVERY = OFF  
GO
ALTER DATABASE [ALITAS EL COMELON SF] SET QUERY_STORE = ON
GO
ALTER DATABASE [ALITAS EL COMELON SF] SET QUERY_STORE (OPERATION_MODE = READ_WRITE, CLEANUP_POLICY = (STALE_QUERY_THRESHOLD_DAYS = 30), DATA_FLUSH_INTERVAL_SECONDS = 900, INTERVAL_LENGTH_MINUTES = 60, MAX_STORAGE_SIZE_MB = 1000, QUERY_CAPTURE_MODE = AUTO, SIZE_BASED_CLEANUP_MODE = AUTO, MAX_PLANS_PER_QUERY = 200, WAIT_STATS_CAPTURE_MODE = ON)
GO
USE [ALITAS EL COMELON SF]
GO
/****** Object:  Table [dbo].[auth_group]    Script Date: 2/2/2026 09:13:33 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[auth_group](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[name] [nvarchar](150) COLLATE Modern_Spanish_CI_AS NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[auth_group_permissions]    Script Date: 2/2/2026 09:13:33 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[auth_group_permissions](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[group_id] [int] NOT NULL,
	[permission_id] [int] NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[auth_permission]    Script Date: 2/2/2026 09:13:33 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[auth_permission](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[name] [nvarchar](255) COLLATE Modern_Spanish_CI_AS NOT NULL,
	[content_type_id] [int] NOT NULL,
	[codename] [nvarchar](100) COLLATE Modern_Spanish_CI_AS NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[auth_user]    Script Date: 2/2/2026 09:13:33 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[auth_user](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[password] [nvarchar](128) COLLATE Modern_Spanish_CI_AS NOT NULL,
	[last_login] [datetimeoffset](7) NULL,
	[is_superuser] [bit] NOT NULL,
	[username] [nvarchar](150) COLLATE Modern_Spanish_CI_AS NOT NULL,
	[first_name] [nvarchar](150) COLLATE Modern_Spanish_CI_AS NOT NULL,
	[last_name] [nvarchar](150) COLLATE Modern_Spanish_CI_AS NOT NULL,
	[email] [nvarchar](254) COLLATE Modern_Spanish_CI_AS NOT NULL,
	[is_staff] [bit] NOT NULL,
	[is_active] [bit] NOT NULL,
	[date_joined] [datetimeoffset](7) NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[auth_user_groups]    Script Date: 2/2/2026 09:13:33 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[auth_user_groups](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[user_id] [int] NOT NULL,
	[group_id] [int] NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[auth_user_user_permissions]    Script Date: 2/2/2026 09:13:33 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[auth_user_user_permissions](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[user_id] [int] NOT NULL,
	[permission_id] [int] NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[CAI]    Script Date: 2/2/2026 09:13:33 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[CAI](
	[ID_Cai] [int] IDENTITY(1,1) NOT FOR REPLICATION NOT NULL,
	[Fecha_Emision] [date] NOT NULL,
	[Fecha_Final] [date] NOT NULL,
	[ID_sucursal] [int] NOT NULL,
	[Secuencia] [int] NOT NULL,
	[estado] [tinyint] NOT NULL,
	[Rango_Inicial] [int] NOT NULL,
	[rango_final] [int] NOT NULL,
	[num_cai] [varchar](50) COLLATE Modern_Spanish_CI_AS NULL,
 CONSTRAINT [PK_Cai] PRIMARY KEY CLUSTERED 
(
	[ID_Cai] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[CAI_Historico]    Script Date: 2/2/2026 09:13:33 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[CAI_Historico](
	[ID_Cai_Historico] [int] IDENTITY(1,1) NOT NULL,
	[ID_Cai] [int] NOT NULL,
	[Fecha_Registro] [datetime] NOT NULL,
	[Fecha_Emision] [date] NOT NULL,
	[Fecha_Final] [date] NOT NULL,
	[Rango_Inicial] [int] NOT NULL,
	[Rango_Final] [int] NOT NULL,
	[Secuencia] [int] NOT NULL,
	[estado] [tinyint] NOT NULL,
	[ID_sucursal] [int] NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[ID_Cai_Historico] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Carrito]    Script Date: 2/2/2026 09:13:33 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Carrito](
	[ID_Carrito] [int] IDENTITY(1,1) NOT NULL,
	[ID_Usuario_ClienteF] [int] NOT NULL,
	[ID_IN_RE] [int] NOT NULL,
	[Cantidad] [int] NOT NULL,
	[total] [numeric](10, 2) NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[ID_Carrito] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[categoria_recetas]    Script Date: 2/2/2026 09:13:33 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[categoria_recetas](
	[id_categoria_receta] [int] IDENTITY(1,1) NOT NULL,
	[Nombre_categoria_receta] [nvarchar](100) COLLATE Modern_Spanish_CI_AS NOT NULL,
	[descripcion] [nvarchar](255) COLLATE Modern_Spanish_CI_AS NULL,
PRIMARY KEY CLUSTERED 
(
	[id_categoria_receta] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[categorias]    Script Date: 2/2/2026 09:13:33 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[categorias](
	[ID_Categoria] [int] IDENTITY(1,1) NOT FOR REPLICATION NOT NULL,
	[Nombre_categoria] [varchar](50) COLLATE Modern_Spanish_CI_AS NOT NULL,
	[descripcion] [varchar](255) COLLATE Modern_Spanish_CI_AS NULL,
	[estado] [tinyint] NOT NULL,
	[tipo] [tinyint] NOT NULL,
 CONSTRAINT [PK_categoria] PRIMARY KEY CLUSTERED 
(
	[ID_Categoria] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[clientes_documento]    Script Date: 2/2/2026 09:13:33 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[clientes_documento](
	[ID_documento] [int] IDENTITY(1,1) NOT FOR REPLICATION NOT NULL,
	[valor documento] [varchar](50) COLLATE Modern_Spanish_CI_AS NOT NULL,
	[ID_Usuario_ClienteF] [int] NOT NULL,
	[tipo_doc] [int] NOT NULL,
 CONSTRAINT [PK_cliente_documento] PRIMARY KEY CLUSTERED 
(
	[ID_documento] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[cocineros]    Script Date: 2/2/2026 09:13:33 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[cocineros](
	[ID_Cocinero] [int] IDENTITY(1,1) NOT FOR REPLICATION NOT NULL,
	[Nombre] [varchar](50) COLLATE Modern_Spanish_CI_AS NOT NULL,
	[Apellido] [varchar](50) COLLATE Modern_Spanish_CI_AS NOT NULL,
	[activo] [tinyint] NOT NULL,
	[ID_Jefe_de_cocina] [int] NOT NULL,
	[Username] [varchar](50) COLLATE Modern_Spanish_CI_AS NOT NULL,
	[Password] [varchar](50) COLLATE Modern_Spanish_CI_AS NOT NULL,
	[ID_sucursal] [int] NOT NULL,
	[descripcion] [varchar](200) COLLATE Modern_Spanish_CI_AS NULL,
 CONSTRAINT [PK_Cocinero] PRIMARY KEY CLUSTERED 
(
	[ID_Cocinero] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[detalle_compra]    Script Date: 2/2/2026 09:13:33 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[detalle_compra](
	[ID_detalle_compra] [int] IDENTITY(1,1) NOT FOR REPLICATION NOT NULL,
	[subtotal] [decimal](10, 2) NOT NULL,
	[precio_unitario] [decimal](10, 2) NOT NULL,
	[Estado] [tinyint] NOT NULL,
	[ID_CompraP] [int] NOT NULL,
 CONSTRAINT [PK_detalle_compra] PRIMARY KEY CLUSTERED 
(
	[ID_detalle_compra] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Detalle_Venta_Cliente]    Script Date: 2/2/2026 09:13:33 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Detalle_Venta_Cliente](
	[ID_Venta_cliente] [int] IDENTITY(1,1) NOT FOR REPLICATION NOT NULL,
	[Descripcion] [varchar](50) COLLATE Modern_Spanish_CI_AS NOT NULL,
	[ID_Orden_cliente] [int] NOT NULL,
	[Numero_correlativo_sar] [varchar](50) COLLATE Modern_Spanish_CI_AS NOT NULL,
	[Importe_exonerado] [decimal](10, 2) NOT NULL,
	[Numero_registro_SAG] [varchar](50) COLLATE Modern_Spanish_CI_AS NOT NULL,
	[Numero_registro_exonerado] [decimal](10, 2) NOT NULL,
	[Fecha_emisionn] [date] NOT NULL,
	[estado] [tinyint] NOT NULL,
 CONSTRAINT [PK_Detalle_Venta_Cliente] PRIMARY KEY CLUSTERED 
(
	[ID_Venta_cliente] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Detalles_de_pago]    Script Date: 2/2/2026 09:13:33 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Detalles_de_pago](
	[ID_TIP_PAG] [int] IDENTITY(1,1) NOT FOR REPLICATION NOT NULL,
	[ID_Tipo_De_Pago] [int] NOT NULL,
	[descripcion] [varchar](50) COLLATE Modern_Spanish_CI_AS NOT NULL,
	[ID_Pago] [int] NOT NULL,
 CONSTRAINT [PK_TIP_PAG] PRIMARY KEY CLUSTERED 
(
	[ID_TIP_PAG] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Direccion_de_los_proveedores]    Script Date: 2/2/2026 09:13:33 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Direccion_de_los_proveedores](
	[ID_DI_PR] [int] IDENTITY(1,1) NOT FOR REPLICATION NOT NULL,
	[ID_Proveedor] [int] NOT NULL,
	[Descripcion] [varchar](50) COLLATE Modern_Spanish_CI_AS NOT NULL,
	[ID_Direccion] [int] NOT NULL,
 CONSTRAINT [PK_DI_PR] PRIMARY KEY CLUSTERED 
(
	[ID_DI_PR] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Direccion_del_cliente]    Script Date: 2/2/2026 09:13:33 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Direccion_del_cliente](
	[ID_US_CO] [int] IDENTITY(1,1) NOT FOR REPLICATION NOT NULL,
	[ID_Usuario_ClienteF] [int] NOT NULL,
	[ID_Direccion] [int] NOT NULL,
 CONSTRAINT [PK_US_CO] PRIMARY KEY CLUSTERED 
(
	[ID_US_CO] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Direccion_del_empleado]    Script Date: 2/2/2026 09:13:33 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Direccion_del_empleado](
	[ID_Empleado_Direccion] [int] IDENTITY(1,1) NOT NULL,
	[ID_Empleado] [int] NOT NULL,
	[ID_Direccion] [int] NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[ID_Empleado_Direccion] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Direcciones]    Script Date: 2/2/2026 09:13:33 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Direcciones](
	[ID_Direccion] [int] IDENTITY(1,1) NOT FOR REPLICATION NOT NULL,
	[descripcion] [varchar](255) COLLATE Modern_Spanish_CI_AS NOT NULL,
 CONSTRAINT [PK_Direccion] PRIMARY KEY CLUSTERED 
(
	[ID_Direccion] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[django_admin_log]    Script Date: 2/2/2026 09:13:33 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[django_admin_log](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[action_time] [datetimeoffset](7) NOT NULL,
	[object_id] [nvarchar](max) COLLATE Modern_Spanish_CI_AS NULL,
	[object_repr] [nvarchar](200) COLLATE Modern_Spanish_CI_AS NOT NULL,
	[action_flag] [smallint] NOT NULL,
	[change_message] [nvarchar](max) COLLATE Modern_Spanish_CI_AS NOT NULL,
	[content_type_id] [int] NULL,
	[user_id] [int] NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[django_content_type]    Script Date: 2/2/2026 09:13:33 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[django_content_type](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[app_label] [nvarchar](100) COLLATE Modern_Spanish_CI_AS NOT NULL,
	[model] [nvarchar](100) COLLATE Modern_Spanish_CI_AS NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[django_migrations]    Script Date: 2/2/2026 09:13:33 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[django_migrations](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[app] [nvarchar](255) COLLATE Modern_Spanish_CI_AS NOT NULL,
	[name] [nvarchar](255) COLLATE Modern_Spanish_CI_AS NOT NULL,
	[applied] [datetimeoffset](7) NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[django_session]    Script Date: 2/2/2026 09:13:33 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[django_session](
	[session_key] [nvarchar](40) COLLATE Modern_Spanish_CI_AS NOT NULL,
	[session_data] [nvarchar](max) COLLATE Modern_Spanish_CI_AS NOT NULL,
	[expire_date] [datetimeoffset](7) NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[session_key] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Empleado]    Script Date: 2/2/2026 09:13:33 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Empleado](
	[ID_Empleado] [int] IDENTITY(1,1) NOT NULL,
	[Nombre] [varchar](100) COLLATE Modern_Spanish_CI_AS NOT NULL,
	[Apellido] [varchar](100) COLLATE Modern_Spanish_CI_AS NOT NULL,
	[Username] [varchar](50) COLLATE Modern_Spanish_CI_AS NOT NULL,
	[Password] [varchar](255) COLLATE Modern_Spanish_CI_AS NOT NULL,
	[Telefono] [varchar](20) COLLATE Modern_Spanish_CI_AS NULL,
	[ID_Puesto] [int] NOT NULL,
	[estado] [int] NOT NULL,
	[ID_sucursal] [int] NOT NULL,
	[Email] [varchar](150) COLLATE Modern_Spanish_CI_AS NULL,
PRIMARY KEY CLUSTERED 
(
	[ID_Empleado] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Empleado_documento]    Script Date: 2/2/2026 09:13:33 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Empleado_documento](
	[ID_empleado_documento] [int] IDENTITY(1,1) NOT FOR REPLICATION NOT NULL,
	[tipo_doc] [int] NOT NULL,
	[ID_Empleado] [int] NOT NULL,
 CONSTRAINT [PK_Empleado_documento] PRIMARY KEY CLUSTERED 
(
	[ID_empleado_documento] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Factura_Detalle]    Script Date: 2/2/2026 09:13:33 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Factura_Detalle](
	[ID_Detalle] [int] IDENTITY(1,1) NOT NULL,
	[ID_Parametro] [int] NOT NULL,
	[ID_IN_RE] [int] NOT NULL,
	[Descripcion] [varchar](100) COLLATE Modern_Spanish_CI_AS NOT NULL,
	[Cantidad] [int] NOT NULL,
	[Precio_unitario] [numeric](18, 2) NOT NULL,
	[Subtotal_linea] [numeric](18, 2) NOT NULL,
	[Impuesto_linea] [numeric](18, 2) NOT NULL,
 CONSTRAINT [PK_Factura_Detalle] PRIMARY KEY CLUSTERED 
(
	[ID_Detalle] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Facturas]    Script Date: 2/2/2026 09:13:33 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Facturas](
	[ID_Parametro] [int] IDENTITY(1,1) NOT NULL,
	[Numero_Factura] [varchar](19) COLLATE Modern_Spanish_CI_AS NOT NULL,
	[Fecha_Emision] [datetime] NOT NULL,
	[ID_Empleado] [int] NOT NULL,
	[ID_Cai] [int] NOT NULL,
	[Subtotal] [money] NOT NULL,
	[Descuento] [money] NOT NULL,
	[Impuesto] [money] NOT NULL,
	[Total_a_pagar] [money] NOT NULL,
	[ID_Usuario_ClienteF] [int] NULL,
	[ID_pago] [int] NULL,
 CONSTRAINT [PK_Facturas] PRIMARY KEY CLUSTERED 
(
	[ID_Parametro] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Gerentes]    Script Date: 2/2/2026 09:13:33 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Gerentes](
	[ID_gerente] [int] IDENTITY(1,1) NOT FOR REPLICATION NOT NULL,
	[Username] [varchar](50) COLLATE Modern_Spanish_CI_AS NOT NULL,
	[Password] [varchar](50) COLLATE Modern_Spanish_CI_AS NOT NULL,
	[ID_sucursal] [int] NOT NULL,
 CONSTRAINT [PK_gerente] PRIMARY KEY CLUSTERED 
(
	[ID_gerente] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[historial_ordenes_repartidor]    Script Date: 2/2/2026 09:13:33 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[historial_ordenes_repartidor](
	[ID_Historial] [int] IDENTITY(1,1) NOT NULL,
	[ID_Orden] [int] NOT NULL,
	[ID_Repartidor] [int] NOT NULL,
	[Estado_Final] [tinyint] NOT NULL,
	[Fecha_Finalizacion] [datetime2](0) NOT NULL,
	[Observacion] [varchar](300) COLLATE Modern_Spanish_CI_AS NULL,
PRIMARY KEY CLUSTERED 
(
	[ID_Historial] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[IM_FA]    Script Date: 2/2/2026 09:13:33 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[IM_FA](
	[ID_IM_FA] [int] IDENTITY(1,1) NOT FOR REPLICATION NOT NULL,
	[ID_Impuesto] [int] NOT NULL,
	[ID_Parametro] [int] NOT NULL,
 CONSTRAINT [PK_IM_FA] PRIMARY KEY CLUSTERED 
(
	[ID_IM_FA] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Impuesto_Categoria]    Script Date: 2/2/2026 09:13:33 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Impuesto_Categoria](
	[ID_Impuesto_Categoria] [int] IDENTITY(1,1) NOT NULL,
	[ID_Impuesto] [int] NOT NULL,
	[ID_Categoria] [int] NOT NULL,
	[Activo] [tinyint] NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[ID_Impuesto_Categoria] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Impuesto_tasa_historica]    Script Date: 2/2/2026 09:13:33 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Impuesto_tasa_historica](
	[ID_Impuesto_historico] [int] IDENTITY(1,1) NOT NULL,
	[ID_Impuesto] [int] NOT NULL,
	[fecha_inicio] [datetime] NOT NULL,
	[fecha_fin] [datetime] NULL,
	[tasa] [numeric](10, 2) NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[ID_Impuesto_historico] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Impuestos]    Script Date: 2/2/2026 09:13:33 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Impuestos](
	[ID_Impuesto] [int] IDENTITY(1,1) NOT FOR REPLICATION NOT NULL,
	[Nombre_Impuesto] [varchar](50) COLLATE Modern_Spanish_CI_AS NOT NULL,
	[tasa] [decimal](10, 2) NOT NULL,
	[descripcion] [varchar](50) COLLATE Modern_Spanish_CI_AS NOT NULL,
	[activo] [tinyint] NOT NULL,
	[ID_Categoria] [int] NOT NULL,
 CONSTRAINT [PK_Impuesto] PRIMARY KEY CLUSTERED 
(
	[ID_Impuesto] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[IN_RE]    Script Date: 2/2/2026 09:13:33 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[IN_RE](
	[ID_IN_RE] [int] IDENTITY(1,1) NOT FOR REPLICATION NOT NULL,
	[Activo] [tinyint] NOT NULL,
	[ID_Insumo] [int] NOT NULL,
	[ID_Receta] [int] NULL,
	[cantidad_usada] [decimal](10, 2) NOT NULL,
	[precio_final] [money] NULL,
	[ID_Unidad] [int] NULL,
	[ID_sucursal] [int] NOT NULL,
 CONSTRAINT [PK_IN_RE] PRIMARY KEY CLUSTERED 
(
	[ID_IN_RE] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Insumo_Precio_historico]    Script Date: 2/2/2026 09:13:33 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Insumo_Precio_historico](
	[ID_Insumo_precio_historico] [int] IDENTITY(1,1) NOT FOR REPLICATION NOT NULL,
	[ID_Insumo] [int] NOT NULL,
	[fecha_inicio] [date] NOT NULL,
	[fecha_fin] [datetime] NULL,
	[Precio] [decimal](18, 0) NOT NULL,
 CONSTRAINT [PK_Precio_historico] PRIMARY KEY CLUSTERED 
(
	[ID_Insumo_precio_historico] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Insumos]    Script Date: 2/2/2026 09:13:33 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Insumos](
	[ID_Insumo] [int] IDENTITY(1,1) NOT FOR REPLICATION NOT NULL,
	[ID_Unidad] [int] NOT NULL,
	[Nombre_insumo] [varchar](50) COLLATE Modern_Spanish_CI_AS NOT NULL,
	[stock_total] [float] NOT NULL,
	[stock_minimo] [float] NOT NULL,
	[precio_lempiras] [decimal](10, 2) NOT NULL,
	[ID_Categoria] [int] NOT NULL,
	[peso_individual] [decimal](10, 2) NULL,
	[precio_base] [decimal](18, 2) NULL,
	[stock_maximo] [float] NULL,
	[ID_sucursal] [int] NOT NULL,
 CONSTRAINT [PK_Insumo] PRIMARY KEY CLUSTERED 
(
	[ID_Insumo] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Jefe_de_cocina]    Script Date: 2/2/2026 09:13:33 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Jefe_de_cocina](
	[ID_Jefe_de_cocina] [int] IDENTITY(1,1) NOT FOR REPLICATION NOT NULL,
	[Nombre] [varchar](50) COLLATE Modern_Spanish_CI_AS NOT NULL,
	[apellido] [varchar](50) COLLATE Modern_Spanish_CI_AS NOT NULL,
	[descripcion] [varchar](50) COLLATE Modern_Spanish_CI_AS NOT NULL,
	[activo] [tinyint] NOT NULL,
	[Username] [varchar](50) COLLATE Modern_Spanish_CI_AS NOT NULL,
	[Password] [varchar](50) COLLATE Modern_Spanish_CI_AS NOT NULL,
	[ID_sucursal] [int] NOT NULL,
 CONSTRAINT [PK_Jefe_de_cocina] PRIMARY KEY CLUSTERED 
(
	[ID_Jefe_de_cocina] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Metodo_de_pago]    Script Date: 2/2/2026 09:13:33 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Metodo_de_pago](
	[ID_Metodo_de_pago] [int] IDENTITY(1,1) NOT NULL,
	[Tipo] [tinyint] NOT NULL,
	[Numero_Tarjeta] [char](16) COLLATE Modern_Spanish_CI_AS NULL,
	[Descripcion] [varchar](50) COLLATE Modern_Spanish_CI_AS NULL,
	[ID_Usuario_ClienteF] [int] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID_Metodo_de_pago] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Metodos_de_pago]    Script Date: 2/2/2026 09:13:33 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Metodos_de_pago](
	[ID_Metodo_de_pago] [int] IDENTITY(1,1) NOT NULL,
	[Tipo] [int] NOT NULL,
	[tarjeta] [varchar](16) COLLATE Modern_Spanish_CI_AS NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[ID_Metodo_de_pago] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Metodos_money]    Script Date: 2/2/2026 09:13:33 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Metodos_money](
	[ID_Metodo] [int] IDENTITY(1,1) NOT NULL,
	[Nombre] [varchar](50) COLLATE Modern_Spanish_CI_AS NOT NULL,
	[Tipo] [tinyint] NOT NULL,
	[Descripcion] [varchar](255) COLLATE Modern_Spanish_CI_AS NULL,
PRIMARY KEY CLUSTERED 
(
	[ID_Metodo] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[ORD_REC]    Script Date: 2/2/2026 09:13:33 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[ORD_REC](
	[ID_ORD_RECETA] [int] IDENTITY(1,1) NOT FOR REPLICATION NOT NULL,
	[Estado] [tinyint] NOT NULL,
	[ID_Orden_cliente] [int] NOT NULL,
	[ID_Repartidor] [int] NOT NULL,
	[ID_Receta] [int] NOT NULL,
	[ID_Parametro] [int] NOT NULL,
 CONSTRAINT [PK_ORD_RECETA] PRIMARY KEY CLUSTERED 
(
	[ID_ORD_RECETA] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Orden_Cliente]    Script Date: 2/2/2026 09:13:33 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Orden_Cliente](
	[ID_Orden_cliente] [int] IDENTITY(1,1) NOT FOR REPLICATION NOT NULL,
	[Descripcion] [varchar](50) COLLATE Modern_Spanish_CI_AS NOT NULL,
	[Num_Factura] [varchar](50) COLLATE Modern_Spanish_CI_AS NOT NULL,
	[Fecha_orden] [date] NOT NULL,
	[ID_Usuario_ClienteF] [int] NOT NULL,
	[Fecha_esperada] [date] NOT NULL,
	[fecha_recepcion] [date] NOT NULL,
 CONSTRAINT [PK_Orden] PRIMARY KEY CLUSTERED 
(
	[ID_Orden_cliente] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Orden_Compra_a_los_Proveedores]    Script Date: 2/2/2026 09:13:33 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Orden_Compra_a_los_Proveedores](
	[ID_CompraP] [int] IDENTITY(1,1) NOT FOR REPLICATION NOT NULL,
	[fecha_orden] [datetime] NOT NULL,
	[fecha_esperada] [datetime] NOT NULL,
	[estado] [tinyint] NOT NULL,
	[fecha_Recepcion] [datetime] NOT NULL,
	[Num_factura_proveida] [varchar](50) COLLATE Modern_Spanish_CI_AS NOT NULL,
	[ID_Proveedor] [int] NOT NULL,
	[ID_Insumo] [int] NOT NULL,
	[ID_Parametro] [int] NOT NULL,
 CONSTRAINT [PK_CompraP] PRIMARY KEY CLUSTERED 
(
	[ID_CompraP] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Orden_Entrega]    Script Date: 2/2/2026 09:13:33 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Orden_Entrega](
	[ID_Orden_Entrega] [int] IDENTITY(1,1) NOT NULL,
	[ID_Parametro] [int] NOT NULL,
	[Numero_Factura] [varchar](19) COLLATE Modern_Spanish_CI_AS NOT NULL,
	[ID_Usuario_ClienteF] [int] NOT NULL,
	[nombre] [varchar](50) COLLATE Modern_Spanish_CI_AS NOT NULL,
	[apellido] [varchar](50) COLLATE Modern_Spanish_CI_AS NOT NULL,
	[ID_US_CO] [int] NOT NULL,
	[ID_Direccion] [int] NOT NULL,
	[descripcion] [varchar](255) COLLATE Modern_Spanish_CI_AS NOT NULL,
	[telefono] [varchar](50) COLLATE Modern_Spanish_CI_AS NOT NULL,
	[ID_sucursal] [int] NOT NULL,
	[ID_Empleado_Repartidor] [int] NOT NULL,
	[estado] [tinyint] NOT NULL,
	[Fecha_Creacion] [datetime] NOT NULL,
	[Motivo_Cancelacion] [varchar](255) COLLATE Modern_Spanish_CI_AS NULL,
 CONSTRAINT [PK_Orden_Entrega] PRIMARY KEY CLUSTERED 
(
	[ID_Orden_Entrega] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Ordenes_Proveedores]    Script Date: 2/2/2026 09:13:33 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Ordenes_Proveedores](
	[ID_Orden_Proveedor] [int] IDENTITY(1,1) NOT NULL,
	[ID_Proveedor] [int] NOT NULL,
	[ID_Empleado_Encargado] [int] NOT NULL,
	[ID_Sucursal] [int] NOT NULL,
	[Fecha_Inicio] [datetime2](0) NOT NULL,
	[Fecha_Estimada] [datetime2](0) NULL,
	[Fecha_Entregado] [datetime2](0) NULL,
	[Estado] [tinyint] NOT NULL,
	[Comentarios] [varchar](300) COLLATE Modern_Spanish_CI_AS NULL,
	[ID_Unidad] [int] NULL,
	[Inventario_Aplicado] [bit] NOT NULL,
	[Numero_Factura] [varchar](14) COLLATE Modern_Spanish_CI_AS NULL,
PRIMARY KEY CLUSTERED 
(
	[ID_Orden_Proveedor] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Ordenes_Proveedores_Detalle]    Script Date: 2/2/2026 09:13:33 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Ordenes_Proveedores_Detalle](
	[ID_Detalle] [int] IDENTITY(1,1) NOT NULL,
	[ID_Orden_Proveedor] [int] NOT NULL,
	[ID_Insumo] [int] NOT NULL,
	[ID_Unidad] [int] NOT NULL,
	[Cantidad_Solicitada] [float] NOT NULL,
	[Cantidad_Recibida] [float] NULL,
	[ID_Unidad_Recibida] [int] NULL,
 CONSTRAINT [PK_Ordenes_Proveedores_Detalle] PRIMARY KEY CLUSTERED 
(
	[ID_Detalle] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[OrdenesProv_Detalle]    Script Date: 2/2/2026 09:13:33 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[OrdenesProv_Detalle](
	[ID_OrdenProv_Detalle] [int] IDENTITY(1,1) NOT NULL,
	[ID_OrdenProv] [int] NOT NULL,
	[ID_Insumo] [int] NOT NULL,
	[Cantidad_Solicitada] [decimal](10, 2) NOT NULL,
	[ID_Unidad] [int] NOT NULL,
	[Cantidad_Recibida] [decimal](10, 2) NULL,
PRIMARY KEY CLUSTERED 
(
	[ID_OrdenProv_Detalle] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[pago_detalle]    Script Date: 2/2/2026 09:13:33 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[pago_detalle](
	[ID_pago] [int] IDENTITY(1,1) NOT NULL,
	[ID_Metodo] [int] NOT NULL,
	[Efectivo] [decimal](18, 2) NULL,
	[Numero_tarjeta] [varchar](4) COLLATE Modern_Spanish_CI_AS NULL,
 CONSTRAINT [PK_pago_detalle] PRIMARY KEY CLUSTERED 
(
	[ID_pago] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Pagos]    Script Date: 2/2/2026 09:13:33 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Pagos](
	[ID_Pago] [int] IDENTITY(1,1) NOT FOR REPLICATION NOT NULL,
	[Monto] [money] NOT NULL,
	[activo] [tinyint] NOT NULL,
	[descripcion] [varchar](50) COLLATE Modern_Spanish_CI_AS NOT NULL,
	[ID_Parametro] [int] NOT NULL,
 CONSTRAINT [PK_Pago] PRIMARY KEY CLUSTERED 
(
	[ID_Pago] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Pagos_cliente]    Script Date: 2/2/2026 09:13:33 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Pagos_cliente](
	[ID_Pago] [int] IDENTITY(1,1) NOT NULL,
	[ID_Usuario_ClienteF] [int] NOT NULL,
	[ID_Metodo] [int] NOT NULL,
	[Cantidad] [decimal](10, 2) NULL,
	[Numero_tarjeta] [char](4) COLLATE Modern_Spanish_CI_AS NULL,
	[a_nombre_de] [varchar](50) COLLATE Modern_Spanish_CI_AS NULL,
PRIMARY KEY CLUSTERED 
(
	[ID_Pago] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Parametros_SAR]    Script Date: 2/2/2026 09:13:33 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Parametros_SAR](
	[ID_Parametro] [int] IDENTITY(1,1) NOT NULL,
	[Parametro] [varchar](50) COLLATE Modern_Spanish_CI_AS NOT NULL,
	[Valor] [varchar](50) COLLATE Modern_Spanish_CI_AS NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[ID_Parametro] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Proveedor_documento]    Script Date: 2/2/2026 09:13:33 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Proveedor_documento](
	[ID_proveedor_documento] [int] IDENTITY(1,1) NOT FOR REPLICATION NOT NULL,
	[descripcion] [varchar](50) COLLATE Modern_Spanish_CI_AS NOT NULL,
	[ID_Proveedor] [int] NOT NULL,
	[tipo_doc] [int] NOT NULL,
 CONSTRAINT [PK_Proveedor_documento] PRIMARY KEY CLUSTERED 
(
	[ID_proveedor_documento] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Proveedor_Insumo]    Script Date: 2/2/2026 09:13:33 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Proveedor_Insumo](
	[ID_Proveedor_Insumo] [int] IDENTITY(1,1) NOT NULL,
	[ID_Proveedor] [int] NOT NULL,
	[ID_Insumo] [int] NOT NULL,
	[Activo] [tinyint] NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[ID_Proveedor_Insumo] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Proveedores]    Script Date: 2/2/2026 09:13:33 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Proveedores](
	[ID_Proveedor] [int] IDENTITY(1,1) NOT FOR REPLICATION NOT NULL,
	[Telefono] [int] NOT NULL,
	[email] [varchar](100) COLLATE Modern_Spanish_CI_AS NOT NULL,
	[activo] [tinyint] NOT NULL,
	[Nombre_Proveedor] [varchar](50) COLLATE Modern_Spanish_CI_AS NOT NULL,
 CONSTRAINT [PK_Proveedor] PRIMARY KEY CLUSTERED 
(
	[ID_Proveedor] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Puesto]    Script Date: 2/2/2026 09:13:33 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Puesto](
	[ID_Puesto] [int] IDENTITY(1,1) NOT NULL,
	[Nombre_Puesto] [varchar](100) COLLATE Modern_Spanish_CI_AS NOT NULL,
	[estado] [int] NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[ID_Puesto] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Recetas]    Script Date: 2/2/2026 09:13:33 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Recetas](
	[ID_Receta] [int] IDENTITY(1,1) NOT FOR REPLICATION NOT NULL,
	[ID_Jefe_de_cocina] [int] NOT NULL,
	[Nombre_receta] [varchar](50) COLLATE Modern_Spanish_CI_AS NOT NULL,
	[Estado] [tinyint] NOT NULL,
	[descripcion] [varchar](500) COLLATE Modern_Spanish_CI_AS NULL,
	[categoria] [tinyint] NULL,
	[descripcion_cliente] [varchar](500) COLLATE Modern_Spanish_CI_AS NULL,
	[ID_sucursal] [int] NOT NULL,
 CONSTRAINT [PK_Receta] PRIMARY KEY CLUSTERED 
(
	[ID_Receta] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[recetas_precio_historico]    Script Date: 2/2/2026 09:13:33 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[recetas_precio_historico](
	[ID_Receta_precio_historico] [int] IDENTITY(1,1) NOT NULL,
	[ID_Receta] [int] NOT NULL,
	[Costo] [decimal](10, 2) NOT NULL,
	[Fecha_inicio] [date] NOT NULL,
	[Fecha_Fin] [date] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID_Receta_precio_historico] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Repartidores]    Script Date: 2/2/2026 09:13:33 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Repartidores](
	[ID_Repartidor] [int] IDENTITY(1,1) NOT FOR REPLICATION NOT NULL,
	[Nombre] [varchar](50) COLLATE Modern_Spanish_CI_AS NOT NULL,
	[telefono] [int] NOT NULL,
	[placa] [varchar](20) COLLATE Modern_Spanish_CI_AS NOT NULL,
	[activo] [tinyint] NOT NULL,
 CONSTRAINT [PK_Repartidores] PRIMARY KEY CLUSTERED 
(
	[ID_Repartidor] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Sucursales]    Script Date: 2/2/2026 09:13:33 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Sucursales](
	[ID_sucursal] [int] IDENTITY(1,1) NOT FOR REPLICATION NOT NULL,
	[Descripcion] [varchar](50) COLLATE Modern_Spanish_CI_AS NOT NULL,
	[ID_Direccion] [int] NOT NULL,
	[estado] [int] NOT NULL,
 CONSTRAINT [PK_sucursal] PRIMARY KEY CLUSTERED 
(
	[ID_sucursal] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Tarea]    Script Date: 2/2/2026 09:13:33 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Tarea](
	[id] [char](32) COLLATE Modern_Spanish_CI_AS NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Tipo_De_Pago]    Script Date: 2/2/2026 09:13:33 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Tipo_De_Pago](
	[ID_Tipo_De_Pago] [int] IDENTITY(1,1) NOT FOR REPLICATION NOT NULL,
	[Nombre] [varchar](50) COLLATE Modern_Spanish_CI_AS NOT NULL,
	[abreviatura] [varchar](10) COLLATE Modern_Spanish_CI_AS NOT NULL,
	[tipo] [tinyint] NOT NULL,
 CONSTRAINT [PK_Table1] PRIMARY KEY CLUSTERED 
(
	[ID_Tipo_De_Pago] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Tipo_documentos]    Script Date: 2/2/2026 09:13:33 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Tipo_documentos](
	[tipo_doc] [int] IDENTITY(1,1) NOT FOR REPLICATION NOT NULL,
	[descripcion] [varchar](50) COLLATE Modern_Spanish_CI_AS NOT NULL,
	[tipo] [tinyint] NULL,
	[numero_documento] [varchar](20) COLLATE Modern_Spanish_CI_AS NOT NULL,
 CONSTRAINT [PK_Tipo_documento] PRIMARY KEY CLUSTERED 
(
	[tipo_doc] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Unidades_Conversion]    Script Date: 2/2/2026 09:13:33 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Unidades_Conversion](
	[ID_Unidad] [int] NOT NULL,
	[Nombre_Unidad] [nvarchar](50) COLLATE Modern_Spanish_CI_AS NULL,
	[Equivalente] [decimal](10, 4) NULL,
	[Tipo] [tinyint] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID_Unidad] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Unidades_medida]    Script Date: 2/2/2026 09:13:33 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Unidades_medida](
	[ID_Unidad] [int] IDENTITY(1,1) NOT FOR REPLICATION NOT NULL,
	[Nombre] [varchar](50) COLLATE Modern_Spanish_CI_AS NOT NULL,
	[abreviatura] [varchar](10) COLLATE Modern_Spanish_CI_AS NOT NULL,
	[Tipo] [tinyint] NOT NULL,
 CONSTRAINT [PK_Unidad] PRIMARY KEY CLUSTERED 
(
	[ID_Unidad] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Usuarios_cliente]    Script Date: 2/2/2026 09:13:33 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Usuarios_cliente](
	[ID_Usuario_ClienteF] [int] IDENTITY(1,1) NOT FOR REPLICATION NOT NULL,
	[Username] [varchar](50) COLLATE Modern_Spanish_CI_AS NOT NULL,
	[password] [varchar](255) COLLATE Modern_Spanish_CI_AS NOT NULL,
	[nombre] [varchar](50) COLLATE Modern_Spanish_CI_AS NOT NULL,
	[apellido] [varchar](50) COLLATE Modern_Spanish_CI_AS NOT NULL,
	[telefono] [varchar](50) COLLATE Modern_Spanish_CI_AS NOT NULL,
	[ID_sucursal] [int] NOT NULL,
	[estado] [tinyint] NOT NULL,
	[correo] [varchar](100) COLLATE Modern_Spanish_CI_AS NULL,
 CONSTRAINT [PK_Usuario] PRIMARY KEY CLUSTERED 
(
	[ID_Usuario_ClienteF] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
SET IDENTITY_INSERT [dbo].[auth_permission] ON 

INSERT [dbo].[auth_permission] ([id], [name], [content_type_id], [codename]) VALUES (1, N'Can add log entry', 1, N'add_logentry')
INSERT [dbo].[auth_permission] ([id], [name], [content_type_id], [codename]) VALUES (2, N'Can change log entry', 1, N'change_logentry')
INSERT [dbo].[auth_permission] ([id], [name], [content_type_id], [codename]) VALUES (3, N'Can delete log entry', 1, N'delete_logentry')
INSERT [dbo].[auth_permission] ([id], [name], [content_type_id], [codename]) VALUES (4, N'Can view log entry', 1, N'view_logentry')
INSERT [dbo].[auth_permission] ([id], [name], [content_type_id], [codename]) VALUES (5, N'Can add permission', 2, N'add_permission')
INSERT [dbo].[auth_permission] ([id], [name], [content_type_id], [codename]) VALUES (6, N'Can change permission', 2, N'change_permission')
INSERT [dbo].[auth_permission] ([id], [name], [content_type_id], [codename]) VALUES (7, N'Can delete permission', 2, N'delete_permission')
INSERT [dbo].[auth_permission] ([id], [name], [content_type_id], [codename]) VALUES (8, N'Can view permission', 2, N'view_permission')
INSERT [dbo].[auth_permission] ([id], [name], [content_type_id], [codename]) VALUES (9, N'Can add group', 3, N'add_group')
INSERT [dbo].[auth_permission] ([id], [name], [content_type_id], [codename]) VALUES (10, N'Can change group', 3, N'change_group')
INSERT [dbo].[auth_permission] ([id], [name], [content_type_id], [codename]) VALUES (11, N'Can delete group', 3, N'delete_group')
INSERT [dbo].[auth_permission] ([id], [name], [content_type_id], [codename]) VALUES (12, N'Can view group', 3, N'view_group')
INSERT [dbo].[auth_permission] ([id], [name], [content_type_id], [codename]) VALUES (13, N'Can add user', 4, N'add_user')
INSERT [dbo].[auth_permission] ([id], [name], [content_type_id], [codename]) VALUES (14, N'Can change user', 4, N'change_user')
INSERT [dbo].[auth_permission] ([id], [name], [content_type_id], [codename]) VALUES (15, N'Can delete user', 4, N'delete_user')
INSERT [dbo].[auth_permission] ([id], [name], [content_type_id], [codename]) VALUES (16, N'Can view user', 4, N'view_user')
INSERT [dbo].[auth_permission] ([id], [name], [content_type_id], [codename]) VALUES (17, N'Can add content type', 5, N'add_contenttype')
INSERT [dbo].[auth_permission] ([id], [name], [content_type_id], [codename]) VALUES (18, N'Can change content type', 5, N'change_contenttype')
INSERT [dbo].[auth_permission] ([id], [name], [content_type_id], [codename]) VALUES (19, N'Can delete content type', 5, N'delete_contenttype')
INSERT [dbo].[auth_permission] ([id], [name], [content_type_id], [codename]) VALUES (20, N'Can view content type', 5, N'view_contenttype')
INSERT [dbo].[auth_permission] ([id], [name], [content_type_id], [codename]) VALUES (21, N'Can add session', 6, N'add_session')
INSERT [dbo].[auth_permission] ([id], [name], [content_type_id], [codename]) VALUES (22, N'Can change session', 6, N'change_session')
INSERT [dbo].[auth_permission] ([id], [name], [content_type_id], [codename]) VALUES (23, N'Can delete session', 6, N'delete_session')
INSERT [dbo].[auth_permission] ([id], [name], [content_type_id], [codename]) VALUES (24, N'Can view session', 6, N'view_session')
INSERT [dbo].[auth_permission] ([id], [name], [content_type_id], [codename]) VALUES (25, N'Can add Tarea', 7, N'add_ejemplo')
INSERT [dbo].[auth_permission] ([id], [name], [content_type_id], [codename]) VALUES (26, N'Can change Tarea', 7, N'change_ejemplo')
INSERT [dbo].[auth_permission] ([id], [name], [content_type_id], [codename]) VALUES (27, N'Can delete Tarea', 7, N'delete_ejemplo')
INSERT [dbo].[auth_permission] ([id], [name], [content_type_id], [codename]) VALUES (28, N'Can view Tarea', 7, N'view_ejemplo')
SET IDENTITY_INSERT [dbo].[auth_permission] OFF
GO
SET IDENTITY_INSERT [dbo].[CAI] ON 

INSERT [dbo].[CAI] ([ID_Cai], [Fecha_Emision], [Fecha_Final], [ID_sucursal], [Secuencia], [estado], [Rango_Inicial], [rango_final], [num_cai]) VALUES (1, CAST(N'2025-11-27' AS Date), CAST(N'2026-07-15' AS Date), 1, 200, 1, 200, 500, N'8ID89S-ADW718-4911DW-ADWQDW-QDQWDQ-DS')
INSERT [dbo].[CAI] ([ID_Cai], [Fecha_Emision], [Fecha_Final], [ID_sucursal], [Secuencia], [estado], [Rango_Inicial], [rango_final], [num_cai]) VALUES (2, CAST(N'2025-11-28' AS Date), CAST(N'2026-07-20' AS Date), 9, 200, 1, 200, 300, N'123456-789123-4567EW-1EWADS-D21D12-XZ')
INSERT [dbo].[CAI] ([ID_Cai], [Fecha_Emision], [Fecha_Final], [ID_sucursal], [Secuencia], [estado], [Rango_Inicial], [rango_final], [num_cai]) VALUES (3, CAST(N'2025-11-28' AS Date), CAST(N'2026-12-03' AS Date), 10, 212, 1, 200, 300, N'FDASWQ-DFSA12-3456DW-1D123S-ADSQDS-SA')
INSERT [dbo].[CAI] ([ID_Cai], [Fecha_Emision], [Fecha_Final], [ID_sucursal], [Secuencia], [estado], [Rango_Inicial], [rango_final], [num_cai]) VALUES (4, CAST(N'2025-12-11' AS Date), CAST(N'2026-09-22' AS Date), 11, 223, 1, 200, 499, N'7KA62S-ADW718-4910DW-1D1312-DSADW1-WQ')
SET IDENTITY_INSERT [dbo].[CAI] OFF
GO
SET IDENTITY_INSERT [dbo].[CAI_Historico] ON 

INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (1, 1, CAST(N'2025-11-28T03:50:54.537' AS DateTime), CAST(N'2025-11-27' AS Date), CAST(N'2026-03-27' AS Date), 200, 300, 201, 1, 1)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (2, 1, CAST(N'2025-11-28T05:05:11.670' AS DateTime), CAST(N'2025-11-27' AS Date), CAST(N'2026-03-27' AS Date), 200, 300, 202, 1, 1)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (12, 1, CAST(N'2025-11-28T21:46:59.990' AS DateTime), CAST(N'2025-11-27' AS Date), CAST(N'2026-03-27' AS Date), 200, 300, 203, 1, 1)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (13, 1, CAST(N'2025-11-28T21:48:40.220' AS DateTime), CAST(N'2025-11-27' AS Date), CAST(N'2026-03-27' AS Date), 200, 300, 250, 1, 1)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (14, 1, CAST(N'2025-11-28T21:49:00.300' AS DateTime), CAST(N'2025-11-27' AS Date), CAST(N'2026-03-27' AS Date), 200, 300, 251, 1, 1)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (15, 2, CAST(N'2025-11-28T22:13:55.117' AS DateTime), CAST(N'2025-11-28' AS Date), CAST(N'2025-11-30' AS Date), 200, 300, 200, 1, 9)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (16, 3, CAST(N'2025-11-28T22:26:25.370' AS DateTime), CAST(N'2025-11-28' AS Date), CAST(N'2025-11-29' AS Date), 200, 300, 200, 1, 10)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (17, 3, CAST(N'2025-11-28T22:27:28.207' AS DateTime), CAST(N'2025-11-28' AS Date), CAST(N'2025-11-29' AS Date), 200, 300, 201, 1, 10)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (18, 3, CAST(N'2025-11-28T23:08:49.503' AS DateTime), CAST(N'2025-11-28' AS Date), CAST(N'2025-11-29' AS Date), 200, 300, 202, 1, 10)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (19, 3, CAST(N'2025-11-28T23:10:44.657' AS DateTime), CAST(N'2025-11-28' AS Date), CAST(N'2025-11-29' AS Date), 200, 300, 203, 1, 10)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (20, 3, CAST(N'2025-11-28T23:11:39.640' AS DateTime), CAST(N'2025-11-28' AS Date), CAST(N'2025-11-29' AS Date), 200, 300, 204, 1, 10)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (21, 1, CAST(N'2025-11-29T01:25:36.097' AS DateTime), CAST(N'2025-11-27' AS Date), CAST(N'2026-03-27' AS Date), 200, 300, 252, 1, 1)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (22, 1, CAST(N'2025-11-29T01:32:02.140' AS DateTime), CAST(N'2025-11-27' AS Date), CAST(N'2026-03-27' AS Date), 200, 300, 253, 1, 1)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (23, 1, CAST(N'2025-11-29T01:32:42.010' AS DateTime), CAST(N'2025-11-27' AS Date), CAST(N'2026-03-27' AS Date), 200, 300, 254, 1, 1)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (24, 3, CAST(N'2025-11-29T01:37:12.550' AS DateTime), CAST(N'2025-11-28' AS Date), CAST(N'2025-11-29' AS Date), 200, 300, 205, 1, 10)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (25, 1, CAST(N'2025-11-29T01:37:39.203' AS DateTime), CAST(N'2025-11-27' AS Date), CAST(N'2026-03-27' AS Date), 200, 300, 255, 1, 1)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (26, 3, CAST(N'2025-11-29T01:38:05.257' AS DateTime), CAST(N'2025-11-28' AS Date), CAST(N'2025-11-29' AS Date), 200, 300, 206, 1, 10)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (27, 3, CAST(N'2025-11-29T01:49:25.757' AS DateTime), CAST(N'2025-11-28' AS Date), CAST(N'2025-11-29' AS Date), 200, 300, 207, 1, 10)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (28, 3, CAST(N'2025-11-29T01:50:09.293' AS DateTime), CAST(N'2025-11-28' AS Date), CAST(N'2025-11-29' AS Date), 200, 300, 208, 1, 10)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (29, 1, CAST(N'2025-11-29T01:50:13.297' AS DateTime), CAST(N'2025-11-27' AS Date), CAST(N'2026-03-27' AS Date), 200, 300, 256, 1, 1)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (30, 1, CAST(N'2025-11-29T01:50:26.193' AS DateTime), CAST(N'2025-11-27' AS Date), CAST(N'2026-03-27' AS Date), 200, 300, 257, 1, 1)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (31, 1, CAST(N'2025-11-29T01:50:27.060' AS DateTime), CAST(N'2025-11-27' AS Date), CAST(N'2026-03-27' AS Date), 200, 300, 258, 1, 1)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (32, 1, CAST(N'2025-11-29T01:50:28.037' AS DateTime), CAST(N'2025-11-27' AS Date), CAST(N'2026-03-27' AS Date), 200, 300, 259, 1, 1)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (33, 1, CAST(N'2025-12-03T00:40:15.867' AS DateTime), CAST(N'2025-11-27' AS Date), CAST(N'2026-03-27' AS Date), 200, 300, 260, 1, 1)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (34, 1, CAST(N'2025-12-03T00:56:58.980' AS DateTime), CAST(N'2025-11-27' AS Date), CAST(N'2026-03-27' AS Date), 200, 300, 261, 1, 1)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (35, 1, CAST(N'2025-12-03T01:06:59.450' AS DateTime), CAST(N'2025-11-27' AS Date), CAST(N'2026-03-27' AS Date), 200, 300, 262, 1, 1)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (36, 1, CAST(N'2025-12-03T01:33:43.490' AS DateTime), CAST(N'2025-11-27' AS Date), CAST(N'2026-03-27' AS Date), 200, 300, 263, 1, 1)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (37, 1, CAST(N'2025-12-03T01:42:41.093' AS DateTime), CAST(N'2025-11-27' AS Date), CAST(N'2026-03-27' AS Date), 200, 300, 264, 1, 1)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (38, 1, CAST(N'2025-12-03T01:43:54.150' AS DateTime), CAST(N'2025-11-27' AS Date), CAST(N'2026-03-27' AS Date), 200, 300, 265, 1, 1)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (39, 1, CAST(N'2025-12-03T01:45:42.250' AS DateTime), CAST(N'2025-11-27' AS Date), CAST(N'2026-03-27' AS Date), 200, 300, 266, 1, 1)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (40, 1, CAST(N'2025-12-03T01:47:17.867' AS DateTime), CAST(N'2025-11-27' AS Date), CAST(N'2026-03-27' AS Date), 200, 300, 267, 1, 1)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (41, 1, CAST(N'2025-12-03T02:15:09.663' AS DateTime), CAST(N'2025-11-27' AS Date), CAST(N'2026-03-27' AS Date), 200, 300, 268, 1, 1)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (42, 1, CAST(N'2025-12-03T02:31:41.147' AS DateTime), CAST(N'2025-11-27' AS Date), CAST(N'2026-03-27' AS Date), 200, 300, 269, 1, 1)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (43, 1, CAST(N'2025-12-03T02:32:31.093' AS DateTime), CAST(N'2025-11-27' AS Date), CAST(N'2026-03-27' AS Date), 200, 300, 270, 1, 1)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (44, 1, CAST(N'2025-12-03T08:36:13.510' AS DateTime), CAST(N'2025-11-27' AS Date), CAST(N'2026-03-27' AS Date), 200, 300, 271, 1, 1)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (45, 1, CAST(N'2025-12-03T09:40:03.413' AS DateTime), CAST(N'2025-11-27' AS Date), CAST(N'2026-03-27' AS Date), 200, 300, 272, 1, 1)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (46, 1, CAST(N'2025-12-03T09:40:48.877' AS DateTime), CAST(N'2025-11-27' AS Date), CAST(N'2026-03-27' AS Date), 200, 300, 273, 1, 1)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (47, 1, CAST(N'2025-12-03T09:51:49.153' AS DateTime), CAST(N'2025-11-27' AS Date), CAST(N'2026-03-27' AS Date), 200, 300, 274, 1, 1)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (48, 1, CAST(N'2025-12-03T09:52:03.357' AS DateTime), CAST(N'2025-11-27' AS Date), CAST(N'2026-03-27' AS Date), 200, 300, 275, 1, 1)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (49, 1, CAST(N'2025-12-03T09:52:07.433' AS DateTime), CAST(N'2025-11-27' AS Date), CAST(N'2026-03-27' AS Date), 200, 300, 276, 1, 1)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (50, 1, CAST(N'2025-12-03T09:52:16.027' AS DateTime), CAST(N'2025-11-27' AS Date), CAST(N'2026-03-27' AS Date), 200, 300, 277, 1, 1)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (51, 1, CAST(N'2025-12-03T09:58:15.897' AS DateTime), CAST(N'2025-11-27' AS Date), CAST(N'2026-03-27' AS Date), 200, 300, 278, 1, 1)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (52, 1, CAST(N'2025-12-03T09:59:14.883' AS DateTime), CAST(N'2025-11-27' AS Date), CAST(N'2026-03-27' AS Date), 200, 300, 279, 1, 1)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (53, 1, CAST(N'2025-12-03T10:08:04.913' AS DateTime), CAST(N'2025-11-27' AS Date), CAST(N'2026-03-27' AS Date), 200, 300, 280, 1, 1)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (54, 1, CAST(N'2025-12-03T10:08:10.363' AS DateTime), CAST(N'2025-11-27' AS Date), CAST(N'2026-03-27' AS Date), 200, 300, 281, 1, 1)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (55, 1, CAST(N'2025-12-03T10:08:17.493' AS DateTime), CAST(N'2025-11-27' AS Date), CAST(N'2026-03-27' AS Date), 200, 300, 282, 1, 1)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (56, 1, CAST(N'2025-12-03T12:40:57.283' AS DateTime), CAST(N'2025-11-27' AS Date), CAST(N'2026-03-27' AS Date), 200, 300, 283, 1, 1)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (59, 1, CAST(N'2025-12-03T13:43:32.210' AS DateTime), CAST(N'2025-11-27' AS Date), CAST(N'2026-03-27' AS Date), 200, 300, 284, 1, 1)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (60, 1, CAST(N'2025-12-03T14:04:19.160' AS DateTime), CAST(N'2025-11-27' AS Date), CAST(N'2026-03-27' AS Date), 200, 300, 285, 1, 1)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (61, 1, CAST(N'2025-12-03T14:04:38.643' AS DateTime), CAST(N'2025-11-27' AS Date), CAST(N'2026-03-27' AS Date), 200, 300, 286, 1, 1)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (62, 1, CAST(N'2025-12-03T14:04:48.837' AS DateTime), CAST(N'2025-11-27' AS Date), CAST(N'2026-03-27' AS Date), 200, 300, 287, 1, 1)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (63, 1, CAST(N'2025-12-03T15:27:46.880' AS DateTime), CAST(N'2025-11-27' AS Date), CAST(N'2026-03-27' AS Date), 200, 300, 299, 1, 1)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (64, 1, CAST(N'2025-12-03T15:28:05.603' AS DateTime), CAST(N'2025-11-27' AS Date), CAST(N'2026-03-27' AS Date), 200, 300, 300, 1, 1)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (65, 1, CAST(N'2025-12-03T15:46:30.273' AS DateTime), CAST(N'2025-11-27' AS Date), CAST(N'2026-03-27' AS Date), 200, 300, 201, 1, 1)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (66, 1, CAST(N'2025-12-03T15:46:50.297' AS DateTime), CAST(N'2025-11-27' AS Date), CAST(N'2026-03-27' AS Date), 200, 300, 202, 1, 1)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (67, 1, CAST(N'2025-12-03T15:47:36.797' AS DateTime), CAST(N'2025-11-27' AS Date), CAST(N'2026-03-27' AS Date), 200, 300, 203, 1, 1)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (68, 1, CAST(N'2025-12-03T15:53:53.677' AS DateTime), CAST(N'2025-11-27' AS Date), CAST(N'2026-03-27' AS Date), 200, 300, 204, 1, 1)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (69, 1, CAST(N'2025-12-04T10:51:45.883' AS DateTime), CAST(N'2025-11-27' AS Date), CAST(N'2026-03-27' AS Date), 200, 300, 205, 1, 1)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (70, 1, CAST(N'2025-12-04T10:57:33.233' AS DateTime), CAST(N'2025-11-27' AS Date), CAST(N'2026-03-27' AS Date), 200, 300, 206, 1, 1)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (71, 1, CAST(N'2025-12-04T11:06:20.503' AS DateTime), CAST(N'2025-11-27' AS Date), CAST(N'2026-03-27' AS Date), 200, 300, 207, 1, 1)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (72, 1, CAST(N'2025-12-04T11:10:49.400' AS DateTime), CAST(N'2025-11-27' AS Date), CAST(N'2026-03-27' AS Date), 200, 300, 208, 1, 1)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (73, 3, CAST(N'2025-12-04T12:19:31.030' AS DateTime), CAST(N'2025-11-28' AS Date), CAST(N'2026-12-03' AS Date), 200, 300, 210, 1, 10)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (74, 3, CAST(N'2025-12-04T12:21:26.187' AS DateTime), CAST(N'2025-11-28' AS Date), CAST(N'2026-12-03' AS Date), 200, 300, 211, 1, 10)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (75, 3, CAST(N'2025-12-04T12:23:08.120' AS DateTime), CAST(N'2025-11-28' AS Date), CAST(N'2026-12-03' AS Date), 200, 300, 212, 1, 10)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (76, 1, CAST(N'2025-12-04T14:04:08.060' AS DateTime), CAST(N'2025-11-27' AS Date), CAST(N'2025-12-12' AS Date), 200, 300, 209, 1, 1)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (77, 1, CAST(N'2025-12-04T15:42:19.260' AS DateTime), CAST(N'2025-11-27' AS Date), CAST(N'2025-12-12' AS Date), 200, 300, 210, 1, 1)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (78, 1, CAST(N'2025-12-04T16:19:39.910' AS DateTime), CAST(N'2025-11-27' AS Date), CAST(N'2025-12-12' AS Date), 200, 300, 211, 1, 1)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (79, 1, CAST(N'2025-12-04T18:07:58.087' AS DateTime), CAST(N'2025-11-27' AS Date), CAST(N'2025-12-12' AS Date), 200, 300, 212, 1, 1)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (80, 1, CAST(N'2025-12-04T18:14:36.653' AS DateTime), CAST(N'2025-11-27' AS Date), CAST(N'2025-12-12' AS Date), 200, 300, 213, 1, 1)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (81, 1, CAST(N'2025-12-04T18:31:13.270' AS DateTime), CAST(N'2025-11-27' AS Date), CAST(N'2025-12-31' AS Date), 200, 300, 214, 1, 1)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (82, 1, CAST(N'2025-12-04T18:31:29.030' AS DateTime), CAST(N'2025-11-27' AS Date), CAST(N'2025-12-31' AS Date), 200, 300, 215, 1, 1)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (83, 1, CAST(N'2025-12-08T08:46:38.857' AS DateTime), CAST(N'2025-11-27' AS Date), CAST(N'2025-12-31' AS Date), 200, 300, 216, 1, 1)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (84, 1, CAST(N'2025-12-08T09:12:47.867' AS DateTime), CAST(N'2025-11-27' AS Date), CAST(N'2025-12-31' AS Date), 200, 300, 217, 1, 1)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (85, 1, CAST(N'2025-12-08T10:00:18.733' AS DateTime), CAST(N'2025-11-27' AS Date), CAST(N'2025-12-31' AS Date), 200, 300, 218, 1, 1)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (86, 1, CAST(N'2025-12-10T08:19:12.890' AS DateTime), CAST(N'2025-11-27' AS Date), CAST(N'2025-12-31' AS Date), 200, 300, 219, 1, 1)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (96, 1, CAST(N'2025-12-11T09:54:59.967' AS DateTime), CAST(N'2025-11-27' AS Date), CAST(N'2025-12-31' AS Date), 200, 300, 220, 1, 1)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (97, 4, CAST(N'2025-12-11T16:10:25.150' AS DateTime), CAST(N'2025-12-11' AS Date), CAST(N'2025-12-31' AS Date), 200, 499, 200, 1, 11)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (98, 4, CAST(N'2025-12-11T16:10:44.217' AS DateTime), CAST(N'2025-12-11' AS Date), CAST(N'2025-12-31' AS Date), 200, 499, 201, 1, 11)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (99, 4, CAST(N'2025-12-12T21:05:34.357' AS DateTime), CAST(N'2025-12-11' AS Date), CAST(N'2025-12-31' AS Date), 200, 499, 202, 1, 11)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (101, 4, CAST(N'2025-12-13T05:12:37.573' AS DateTime), CAST(N'2025-12-11' AS Date), CAST(N'2025-12-31' AS Date), 200, 499, 203, 1, 11)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (102, 4, CAST(N'2025-12-13T05:13:46.853' AS DateTime), CAST(N'2025-12-11' AS Date), CAST(N'2025-12-31' AS Date), 200, 499, 204, 1, 11)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (103, 4, CAST(N'2025-12-13T05:13:51.747' AS DateTime), CAST(N'2025-12-11' AS Date), CAST(N'2025-12-31' AS Date), 200, 499, 205, 1, 11)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (104, 4, CAST(N'2025-12-13T05:30:58.873' AS DateTime), CAST(N'2025-12-11' AS Date), CAST(N'2025-12-31' AS Date), 200, 499, 206, 1, 11)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (105, 4, CAST(N'2025-12-13T05:31:01.890' AS DateTime), CAST(N'2025-12-11' AS Date), CAST(N'2025-12-31' AS Date), 200, 499, 207, 1, 11)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (106, 4, CAST(N'2025-12-14T00:38:17.227' AS DateTime), CAST(N'2025-12-11' AS Date), CAST(N'2025-12-31' AS Date), 200, 499, 208, 1, 11)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (107, 4, CAST(N'2025-12-14T01:05:21.153' AS DateTime), CAST(N'2025-12-11' AS Date), CAST(N'2025-12-31' AS Date), 200, 499, 209, 1, 11)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (108, 4, CAST(N'2025-12-14T01:11:37.210' AS DateTime), CAST(N'2025-12-11' AS Date), CAST(N'2025-12-31' AS Date), 200, 499, 210, 1, 11)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (109, 4, CAST(N'2025-12-14T01:12:04.193' AS DateTime), CAST(N'2025-12-11' AS Date), CAST(N'2025-12-31' AS Date), 200, 499, 211, 1, 11)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (110, 4, CAST(N'2025-12-14T01:15:15.837' AS DateTime), CAST(N'2025-12-11' AS Date), CAST(N'2025-12-31' AS Date), 200, 499, 212, 1, 11)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (111, 4, CAST(N'2025-12-14T01:44:18.373' AS DateTime), CAST(N'2025-12-11' AS Date), CAST(N'2025-12-31' AS Date), 200, 499, 213, 1, 11)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (1106, 4, CAST(N'2025-12-14T04:15:35.223' AS DateTime), CAST(N'2025-12-11' AS Date), CAST(N'2025-12-31' AS Date), 200, 499, 214, 1, 11)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (1107, 4, CAST(N'2025-12-14T08:58:24.793' AS DateTime), CAST(N'2025-12-11' AS Date), CAST(N'2025-12-31' AS Date), 200, 499, 215, 1, 11)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (1108, 4, CAST(N'2025-12-14T09:02:37.553' AS DateTime), CAST(N'2025-12-11' AS Date), CAST(N'2025-12-31' AS Date), 200, 499, 216, 1, 11)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (2107, 4, CAST(N'2025-12-14T12:59:23.990' AS DateTime), CAST(N'2025-12-11' AS Date), CAST(N'2025-12-31' AS Date), 200, 499, 217, 1, 11)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (2108, 4, CAST(N'2025-12-15T01:03:33.663' AS DateTime), CAST(N'2025-12-11' AS Date), CAST(N'2025-12-31' AS Date), 200, 499, 218, 1, 11)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (2109, 4, CAST(N'2025-12-15T02:31:00.327' AS DateTime), CAST(N'2025-12-11' AS Date), CAST(N'2025-12-31' AS Date), 200, 499, 219, 1, 11)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (2110, 4, CAST(N'2025-12-15T02:40:55.223' AS DateTime), CAST(N'2025-12-11' AS Date), CAST(N'2025-12-31' AS Date), 200, 499, 220, 1, 11)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (2111, 4, CAST(N'2025-12-15T03:44:29.920' AS DateTime), CAST(N'2025-12-11' AS Date), CAST(N'2025-12-31' AS Date), 200, 499, 221, 1, 11)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (2112, 4, CAST(N'2025-12-15T03:44:48.637' AS DateTime), CAST(N'2025-12-11' AS Date), CAST(N'2025-12-31' AS Date), 200, 499, 222, 1, 11)
GO
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (2113, 1, CAST(N'2026-01-26T14:32:39.137' AS DateTime), CAST(N'2025-11-27' AS Date), CAST(N'2026-01-26' AS Date), 200, 500, 200, 1, 1)
INSERT [dbo].[CAI_Historico] ([ID_Cai_Historico], [ID_Cai], [Fecha_Registro], [Fecha_Emision], [Fecha_Final], [Rango_Inicial], [Rango_Final], [Secuencia], [estado], [ID_sucursal]) VALUES (2117, 4, CAST(N'2026-02-02T03:36:54.093' AS DateTime), CAST(N'2025-12-11' AS Date), CAST(N'2026-09-22' AS Date), 200, 499, 223, 1, 11)
SET IDENTITY_INSERT [dbo].[CAI_Historico] OFF
GO
SET IDENTITY_INSERT [dbo].[Carrito] ON 

INSERT [dbo].[Carrito] ([ID_Carrito], [ID_Usuario_ClienteF], [ID_IN_RE], [Cantidad], [total]) VALUES (6, 1002, 1296, 1, CAST(17.55 AS Numeric(10, 2)))
INSERT [dbo].[Carrito] ([ID_Carrito], [ID_Usuario_ClienteF], [ID_IN_RE], [Cantidad], [total]) VALUES (25, 1003, 1300, 3, CAST(7.11 AS Numeric(10, 2)))
INSERT [dbo].[Carrito] ([ID_Carrito], [ID_Usuario_ClienteF], [ID_IN_RE], [Cantidad], [total]) VALUES (1028, 1, 1307, 1, CAST(29.40 AS Numeric(10, 2)))
SET IDENTITY_INSERT [dbo].[Carrito] OFF
GO
SET IDENTITY_INSERT [dbo].[categoria_recetas] ON 

INSERT [dbo].[categoria_recetas] ([id_categoria_receta], [Nombre_categoria_receta], [descripcion]) VALUES (1, N'Alitas', N'Categoría que incluye todas las recetas basadas en alitas de pollo con diferentes estilos y sabores.')
INSERT [dbo].[categoria_recetas] ([id_categoria_receta], [Nombre_categoria_receta], [descripcion]) VALUES (2, N'Postres', N'Incluye recetas dulces como pasteles, flanes y repostería variada.')
INSERT [dbo].[categoria_recetas] ([id_categoria_receta], [Nombre_categoria_receta], [descripcion]) VALUES (3, N'Bebidas', N'Recetas de jugos, cócteles, batidos y bebidas frías o calientes.')
INSERT [dbo].[categoria_recetas] ([id_categoria_receta], [Nombre_categoria_receta], [descripcion]) VALUES (4, N'Entradas', N'Platos ligeros que se sirven antes del plato principal.')
INSERT [dbo].[categoria_recetas] ([id_categoria_receta], [Nombre_categoria_receta], [descripcion]) VALUES (5, N'Otro', N'Recetas que no pertenecen a las categorías principales.')
SET IDENTITY_INSERT [dbo].[categoria_recetas] OFF
GO
SET IDENTITY_INSERT [dbo].[categorias] ON 

INSERT [dbo].[categorias] ([ID_Categoria], [Nombre_categoria], [descripcion], [estado], [tipo]) VALUES (1, N'Verduras', N'Productos vegetales frescos y de hoja verde', 1, 1)
INSERT [dbo].[categorias] ([ID_Categoria], [Nombre_categoria], [descripcion], [estado], [tipo]) VALUES (2, N'Carnes', N'Productos cárnicos crudos o procesados', 1, 1)
INSERT [dbo].[categorias] ([ID_Categoria], [Nombre_categoria], [descripcion], [estado], [tipo]) VALUES (3, N'Mariscos', N'Pescados y productos del mar', 1, 1)
INSERT [dbo].[categorias] ([ID_Categoria], [Nombre_categoria], [descripcion], [estado], [tipo]) VALUES (4, N'Cereales', N'Granos básicos y productos derivados', 1, 1)
INSERT [dbo].[categorias] ([ID_Categoria], [Nombre_categoria], [descripcion], [estado], [tipo]) VALUES (5, N'Lácteos', N'Productos derivados de la leche como queso o mantequilla', 1, 1)
INSERT [dbo].[categorias] ([ID_Categoria], [Nombre_categoria], [descripcion], [estado], [tipo]) VALUES (6, N'Frutas', N'Frutas frescas y de temporada', 1, 1)
INSERT [dbo].[categorias] ([ID_Categoria], [Nombre_categoria], [descripcion], [estado], [tipo]) VALUES (7, N'Panadería', N'Productos horneados y de panadería', 1, 1)
INSERT [dbo].[categorias] ([ID_Categoria], [Nombre_categoria], [descripcion], [estado], [tipo]) VALUES (8, N'Salsas', N'Salsas líquidas o espesas para acompañar comidas', 1, 1)
INSERT [dbo].[categorias] ([ID_Categoria], [Nombre_categoria], [descripcion], [estado], [tipo]) VALUES (9, N'Granos', N'Granos secos o molidos usados en la cocina', 1, 1)
INSERT [dbo].[categorias] ([ID_Categoria], [Nombre_categoria], [descripcion], [estado], [tipo]) VALUES (10, N'Bebidas Gaseosas', N'Refrescos embotellados o gaseosos', 1, 1)
INSERT [dbo].[categorias] ([ID_Categoria], [Nombre_categoria], [descripcion], [estado], [tipo]) VALUES (11, N'Verduras Congeladas', N'Verduras procesadas y congeladas', 1, 1)
INSERT [dbo].[categorias] ([ID_Categoria], [Nombre_categoria], [descripcion], [estado], [tipo]) VALUES (12, N'Lácteos y derivados', N'Leche y sus derivados', 1, 1)
INSERT [dbo].[categorias] ([ID_Categoria], [Nombre_categoria], [descripcion], [estado], [tipo]) VALUES (13, N'Aderezos', N'Condimentos y acompañantes para comidas', 1, 1)
INSERT [dbo].[categorias] ([ID_Categoria], [Nombre_categoria], [descripcion], [estado], [tipo]) VALUES (14, N'Bebidas Naturales', N'Jugos y bebidas naturales elaboradas en casa', 1, 1)
INSERT [dbo].[categorias] ([ID_Categoria], [Nombre_categoria], [descripcion], [estado], [tipo]) VALUES (15, N'Especias', N'Condimentos secos y especias en polvo', 1, 1)
INSERT [dbo].[categorias] ([ID_Categoria], [Nombre_categoria], [descripcion], [estado], [tipo]) VALUES (16, N'Aceites', N'Aceites vegetales y derivados', 1, 1)
INSERT [dbo].[categorias] ([ID_Categoria], [Nombre_categoria], [descripcion], [estado], [tipo]) VALUES (17, N'Otros', N'Otros insumos de uso general', 1, 1)
INSERT [dbo].[categorias] ([ID_Categoria], [Nombre_categoria], [descripcion], [estado], [tipo]) VALUES (72, N'Bebidas Alcoholicas', N'bebidas que contienen alcohol', 1, 1)
SET IDENTITY_INSERT [dbo].[categorias] OFF
GO
SET IDENTITY_INSERT [dbo].[cocineros] ON 

INSERT [dbo].[cocineros] ([ID_Cocinero], [Nombre], [Apellido], [activo], [ID_Jefe_de_cocina], [Username], [Password], [ID_sucursal], [descripcion]) VALUES (1, N'Rodrigo', N'alvarez', 1, 1, N'rodrigoalvarez', N'rodrigo190305', 1, NULL)
SET IDENTITY_INSERT [dbo].[cocineros] OFF
GO
SET IDENTITY_INSERT [dbo].[Direccion_del_cliente] ON 

INSERT [dbo].[Direccion_del_cliente] ([ID_US_CO], [ID_Usuario_ClienteF], [ID_Direccion]) VALUES (1, 1, 1010)
INSERT [dbo].[Direccion_del_cliente] ([ID_US_CO], [ID_Usuario_ClienteF], [ID_Direccion]) VALUES (1022, 1, 1011)
INSERT [dbo].[Direccion_del_cliente] ([ID_US_CO], [ID_Usuario_ClienteF], [ID_Direccion]) VALUES (1023, 1, 1012)
INSERT [dbo].[Direccion_del_cliente] ([ID_US_CO], [ID_Usuario_ClienteF], [ID_Direccion]) VALUES (1024, 1003, 1014)
SET IDENTITY_INSERT [dbo].[Direccion_del_cliente] OFF
GO
SET IDENTITY_INSERT [dbo].[Direcciones] ON 

INSERT [dbo].[Direcciones] ([ID_Direccion], [descripcion]) VALUES (1, N'Sucursal principal por residencial plaza 4 casas abajo de empeños aurora')
INSERT [dbo].[Direcciones] ([ID_Direccion], [descripcion]) VALUES (2, N'residencial plaza')
INSERT [dbo].[Direcciones] ([ID_Direccion], [descripcion]) VALUES (3, N'residencial plaza')
INSERT [dbo].[Direcciones] ([ID_Direccion], [descripcion]) VALUES (1007, N'porgds')
INSERT [dbo].[Direcciones] ([ID_Direccion], [descripcion]) VALUES (1008, N'por alli')
INSERT [dbo].[Direcciones] ([ID_Direccion], [descripcion]) VALUES (1009, N'residencial plaza')
INSERT [dbo].[Direcciones] ([ID_Direccion], [descripcion]) VALUES (1010, N'residencial plazas')
INSERT [dbo].[Direcciones] ([ID_Direccion], [descripcion]) VALUES (1011, N'hola adios ejemplo')
INSERT [dbo].[Direcciones] ([ID_Direccion], [descripcion]) VALUES (1012, N'direccion 2')
INSERT [dbo].[Direcciones] ([ID_Direccion], [descripcion]) VALUES (1013, N'Sucursal digital por residencial plaza 4 casas abajo de empeños')
INSERT [dbo].[Direcciones] ([ID_Direccion], [descripcion]) VALUES (1014, N'pedregal')
SET IDENTITY_INSERT [dbo].[Direcciones] OFF
GO
SET IDENTITY_INSERT [dbo].[django_content_type] ON 

INSERT [dbo].[django_content_type] ([id], [app_label], [model]) VALUES (1, N'admin', N'logentry')
INSERT [dbo].[django_content_type] ([id], [app_label], [model]) VALUES (3, N'auth', N'group')
INSERT [dbo].[django_content_type] ([id], [app_label], [model]) VALUES (2, N'auth', N'permission')
INSERT [dbo].[django_content_type] ([id], [app_label], [model]) VALUES (4, N'auth', N'user')
INSERT [dbo].[django_content_type] ([id], [app_label], [model]) VALUES (5, N'contenttypes', N'contenttype')
INSERT [dbo].[django_content_type] ([id], [app_label], [model]) VALUES (7, N'login', N'ejemplo')
INSERT [dbo].[django_content_type] ([id], [app_label], [model]) VALUES (6, N'sessions', N'session')
SET IDENTITY_INSERT [dbo].[django_content_type] OFF
GO
SET IDENTITY_INSERT [dbo].[django_migrations] ON 

INSERT [dbo].[django_migrations] ([id], [app], [name], [applied]) VALUES (1, N'contenttypes', N'0001_initial', CAST(N'2025-11-16T21:22:04.5834460+00:00' AS DateTimeOffset))
INSERT [dbo].[django_migrations] ([id], [app], [name], [applied]) VALUES (2, N'auth', N'0001_initial', CAST(N'2025-11-16T21:22:04.6333690+00:00' AS DateTimeOffset))
INSERT [dbo].[django_migrations] ([id], [app], [name], [applied]) VALUES (3, N'admin', N'0001_initial', CAST(N'2025-11-16T21:22:04.6521620+00:00' AS DateTimeOffset))
INSERT [dbo].[django_migrations] ([id], [app], [name], [applied]) VALUES (4, N'admin', N'0002_logentry_remove_auto_add', CAST(N'2025-11-16T21:22:04.6577960+00:00' AS DateTimeOffset))
INSERT [dbo].[django_migrations] ([id], [app], [name], [applied]) VALUES (5, N'admin', N'0003_logentry_add_action_flag_choices', CAST(N'2025-11-16T21:22:04.6637640+00:00' AS DateTimeOffset))
INSERT [dbo].[django_migrations] ([id], [app], [name], [applied]) VALUES (6, N'contenttypes', N'0002_remove_content_type_name', CAST(N'2025-11-16T21:22:05.0143500+00:00' AS DateTimeOffset))
INSERT [dbo].[django_migrations] ([id], [app], [name], [applied]) VALUES (7, N'auth', N'0002_alter_permission_name_max_length', CAST(N'2025-11-16T21:22:05.0213990+00:00' AS DateTimeOffset))
INSERT [dbo].[django_migrations] ([id], [app], [name], [applied]) VALUES (8, N'auth', N'0003_alter_user_email_max_length', CAST(N'2025-11-16T21:22:05.0294260+00:00' AS DateTimeOffset))
INSERT [dbo].[django_migrations] ([id], [app], [name], [applied]) VALUES (9, N'auth', N'0004_alter_user_username_opts', CAST(N'2025-11-16T21:22:05.0360240+00:00' AS DateTimeOffset))
INSERT [dbo].[django_migrations] ([id], [app], [name], [applied]) VALUES (10, N'auth', N'0005_alter_user_last_login_null', CAST(N'2025-11-16T21:22:05.4063490+00:00' AS DateTimeOffset))
INSERT [dbo].[django_migrations] ([id], [app], [name], [applied]) VALUES (11, N'auth', N'0006_require_contenttypes_0002', CAST(N'2025-11-16T21:22:05.4134810+00:00' AS DateTimeOffset))
INSERT [dbo].[django_migrations] ([id], [app], [name], [applied]) VALUES (12, N'auth', N'0007_alter_validators_add_error_messages', CAST(N'2025-11-16T21:22:05.4189370+00:00' AS DateTimeOffset))
INSERT [dbo].[django_migrations] ([id], [app], [name], [applied]) VALUES (13, N'auth', N'0008_alter_user_username_max_length', CAST(N'2025-11-16T21:22:05.4510070+00:00' AS DateTimeOffset))
INSERT [dbo].[django_migrations] ([id], [app], [name], [applied]) VALUES (14, N'auth', N'0009_alter_user_last_name_max_length', CAST(N'2025-11-16T21:22:05.4579400+00:00' AS DateTimeOffset))
INSERT [dbo].[django_migrations] ([id], [app], [name], [applied]) VALUES (15, N'auth', N'0010_alter_group_name_max_length', CAST(N'2025-11-16T21:22:05.8178390+00:00' AS DateTimeOffset))
INSERT [dbo].[django_migrations] ([id], [app], [name], [applied]) VALUES (16, N'auth', N'0011_update_proxy_permissions', CAST(N'2025-11-16T21:22:05.8178390+00:00' AS DateTimeOffset))
INSERT [dbo].[django_migrations] ([id], [app], [name], [applied]) VALUES (17, N'auth', N'0012_alter_user_first_name_max_length', CAST(N'2025-11-16T21:22:05.8377730+00:00' AS DateTimeOffset))
INSERT [dbo].[django_migrations] ([id], [app], [name], [applied]) VALUES (18, N'sessions', N'0001_initial', CAST(N'2025-11-16T21:22:05.8435410+00:00' AS DateTimeOffset))
INSERT [dbo].[django_migrations] ([id], [app], [name], [applied]) VALUES (19, N'login', N'0001_initial', CAST(N'2025-11-16T21:33:24.7269540+00:00' AS DateTimeOffset))
SET IDENTITY_INSERT [dbo].[django_migrations] OFF
GO
INSERT [dbo].[django_session] ([session_key], [session_data], [expire_date]) VALUES (N'lcecwfntxgi8g7gb6anw720a1uyk3lk7', N'eyJpZCI6MSwidGlwbyI6ImVtcGxlYWRvIiwicHVlc3RvIjoiSmVmZSBkZSBDb2NpbmEifQ:1vKv2C:TqVno2hsbHmfY4YM74RaKKOFrinDIFNcFQozo_lwrKU', CAST(N'2025-12-01T08:56:28.7078540+00:00' AS DateTimeOffset))
GO
SET IDENTITY_INSERT [dbo].[Empleado] ON 

INSERT [dbo].[Empleado] ([ID_Empleado], [Nombre], [Apellido], [Username], [Password], [Telefono], [ID_Puesto], [estado], [ID_sucursal], [Email]) VALUES (1, N'Juan', N'Pérez', N'jefe1', N'K3v!n190305', N'99998887', 1, 1, 1, NULL)
INSERT [dbo].[Empleado] ([ID_Empleado], [Nombre], [Apellido], [Username], [Password], [Telefono], [ID_Puesto], [estado], [ID_sucursal], [Email]) VALUES (2, N'Kevin Alejandro', N'Perez Guillen', N'kevin_ew', N'K!vin190305', N'99998885', 3, 1, 1, NULL)
INSERT [dbo].[Empleado] ([ID_Empleado], [Nombre], [Apellido], [Username], [Password], [Telefono], [ID_Puesto], [estado], [ID_sucursal], [Email]) VALUES (8, N'Dsaa', N'Dsa', N'Dsadwwda', N'K3v!n190305', N'99998886', 6, 0, 1, NULL)
INSERT [dbo].[Empleado] ([ID_Empleado], [Nombre], [Apellido], [Username], [Password], [Telefono], [ID_Puesto], [estado], [ID_sucursal], [Email]) VALUES (9, N'Dsa', N'Dsa', N'Dsa', N'K3v!n190305', N'99998888', 6, 0, 1, NULL)
INSERT [dbo].[Empleado] ([ID_Empleado], [Nombre], [Apellido], [Username], [Password], [Telefono], [ID_Puesto], [estado], [ID_sucursal], [Email]) VALUES (10, N'Ddsa', N'Dsadw', N'dwqsa', N'K3v!n190305', N'99998810', 1, 1, 1, NULL)
INSERT [dbo].[Empleado] ([ID_Empleado], [Nombre], [Apellido], [Username], [Password], [Telefono], [ID_Puesto], [estado], [ID_sucursal], [Email]) VALUES (13, N'Kevin', N'Guillen', N'kevin_cont', N'K3v!n190305', N'99998844', 10, 1, 1, NULL)
INSERT [dbo].[Empleado] ([ID_Empleado], [Nombre], [Apellido], [Username], [Password], [Telefono], [ID_Puesto], [estado], [ID_sucursal], [Email]) VALUES (14, N'Sistema', N'Web', N'web', N'K3v!n190305', N'99990001', 12, 1, 1, NULL)
INSERT [dbo].[Empleado] ([ID_Empleado], [Nombre], [Apellido], [Username], [Password], [Telefono], [ID_Puesto], [estado], [ID_sucursal], [Email]) VALUES (15, N'Sistema', N'Web Dos', N'web2', N'K3v!n190305', N'99991111', 12, 1, 10, NULL)
INSERT [dbo].[Empleado] ([ID_Empleado], [Nombre], [Apellido], [Username], [Password], [Telefono], [ID_Puesto], [estado], [ID_sucursal], [Email]) VALUES (16, N'Kevin', N'Qwerty Uno', N'qwerty', N'K3v!n190305', N'99998576', 13, 1, 1, NULL)
INSERT [dbo].[Empleado] ([ID_Empleado], [Nombre], [Apellido], [Username], [Password], [Telefono], [ID_Puesto], [estado], [ID_sucursal], [Email]) VALUES (17, N'Kevin', N'Qwerty Dos', N'qwerty2', N'K3v!n190305', N'99991212', 13, 1, 10, NULL)
INSERT [dbo].[Empleado] ([ID_Empleado], [Nombre], [Apellido], [Username], [Password], [Telefono], [ID_Puesto], [estado], [ID_sucursal], [Email]) VALUES (18, N'Kevin Alejandro', N'Web Tres', N'webres', N'K3v!n190305', N'99993213', 13, 1, 9, NULL)
INSERT [dbo].[Empleado] ([ID_Empleado], [Nombre], [Apellido], [Username], [Password], [Telefono], [ID_Puesto], [estado], [ID_sucursal], [Email]) VALUES (19, N'Joseline', N'Gomez', N'joseline_g', N'K3v!n190305', N'999988321', 4, 1, 11, N'kevinherg2015@gmail.com')
INSERT [dbo].[Empleado] ([ID_Empleado], [Nombre], [Apellido], [Username], [Password], [Telefono], [ID_Puesto], [estado], [ID_sucursal], [Email]) VALUES (20, N'Local Web', N'Web', N'webeb', N'K3v!n190305', N'99323232', 11, 1, 11, N'kevinherg2030@gmail.com')
INSERT [dbo].[Empleado] ([ID_Empleado], [Nombre], [Apellido], [Username], [Password], [Telefono], [ID_Puesto], [estado], [ID_sucursal], [Email]) VALUES (21, N'Juan', N'Herrera Guillen', N'webebdw', N'K3v!n190305', N'99991112', 13, 1, 11, N'kevinherg2025@gmail.com')
INSERT [dbo].[Empleado] ([ID_Empleado], [Nombre], [Apellido], [Username], [Password], [Telefono], [ID_Puesto], [estado], [ID_sucursal], [Email]) VALUES (22, N'Kevin Alejandros', N'Herrera Guillend', N'kevin_enc', N'K3v!n190305', N'99998654', 14, 1, 11, N'kevinherg2005@gmail.com')
INSERT [dbo].[Empleado] ([ID_Empleado], [Nombre], [Apellido], [Username], [Password], [Telefono], [ID_Puesto], [estado], [ID_sucursal], [Email]) VALUES (23, N'Jefe Kevin', N'Kevin Jefe', N'kevin_jef2', N'K3v!n190305', N'99323132', 1, 1, 11, N'kevinherg5@gmail.com')
INSERT [dbo].[Empleado] ([ID_Empleado], [Nombre], [Apellido], [Username], [Password], [Telefono], [ID_Puesto], [estado], [ID_sucursal], [Email]) VALUES (24, N'Kevin', N'Ger', N'kevin_ger', N'K3v!n190305', N'30320130', 16, 1, 11, N'kevinherg6@gmail.com')
INSERT [dbo].[Empleado] ([ID_Empleado], [Nombre], [Apellido], [Username], [Password], [Telefono], [ID_Puesto], [estado], [ID_sucursal], [Email]) VALUES (25, N'Kevin', N'Gerente Dos', N'kevin_ger2', N'K3v!n190305', N'33323232', 16, 1, 1, N'kevinherg9@gmail.com')
INSERT [dbo].[Empleado] ([ID_Empleado], [Nombre], [Apellido], [Username], [Password], [Telefono], [ID_Puesto], [estado], [ID_sucursal], [Email]) VALUES (26, N'Kevin Alejandro', N'Dsadws', N'kevin_jef', N'K3v!n190305', N'93203232', 1, 1, 1, N'kevinherg12@gmail.com')
SET IDENTITY_INSERT [dbo].[Empleado] OFF
GO
SET IDENTITY_INSERT [dbo].[Empleado_documento] ON 

INSERT [dbo].[Empleado_documento] ([ID_empleado_documento], [tipo_doc], [ID_Empleado]) VALUES (1, 5, 14)
INSERT [dbo].[Empleado_documento] ([ID_empleado_documento], [tipo_doc], [ID_Empleado]) VALUES (2, 6, 15)
INSERT [dbo].[Empleado_documento] ([ID_empleado_documento], [tipo_doc], [ID_Empleado]) VALUES (3, 7, 16)
INSERT [dbo].[Empleado_documento] ([ID_empleado_documento], [tipo_doc], [ID_Empleado]) VALUES (4, 8, 17)
INSERT [dbo].[Empleado_documento] ([ID_empleado_documento], [tipo_doc], [ID_Empleado]) VALUES (5, 9, 18)
INSERT [dbo].[Empleado_documento] ([ID_empleado_documento], [tipo_doc], [ID_Empleado]) VALUES (6, 10, 19)
INSERT [dbo].[Empleado_documento] ([ID_empleado_documento], [tipo_doc], [ID_Empleado]) VALUES (7, 11, 20)
INSERT [dbo].[Empleado_documento] ([ID_empleado_documento], [tipo_doc], [ID_Empleado]) VALUES (8, 12, 21)
INSERT [dbo].[Empleado_documento] ([ID_empleado_documento], [tipo_doc], [ID_Empleado]) VALUES (9, 13, 22)
INSERT [dbo].[Empleado_documento] ([ID_empleado_documento], [tipo_doc], [ID_Empleado]) VALUES (10, 14, 23)
INSERT [dbo].[Empleado_documento] ([ID_empleado_documento], [tipo_doc], [ID_Empleado]) VALUES (11, 15, 24)
INSERT [dbo].[Empleado_documento] ([ID_empleado_documento], [tipo_doc], [ID_Empleado]) VALUES (12, 16, 25)
INSERT [dbo].[Empleado_documento] ([ID_empleado_documento], [tipo_doc], [ID_Empleado]) VALUES (13, 17, 26)
SET IDENTITY_INSERT [dbo].[Empleado_documento] OFF
GO
SET IDENTITY_INSERT [dbo].[Factura_Detalle] ON 

INSERT [dbo].[Factura_Detalle] ([ID_Detalle], [ID_Parametro], [ID_IN_RE], [Descripcion], [Cantidad], [Precio_unitario], [Subtotal_linea], [Impuesto_linea]) VALUES (2113, 2088, 1304, N'Alitas BBQ', 1, CAST(5.69 AS Numeric(18, 2)), CAST(21.66 AS Numeric(18, 2)), CAST(3.25 AS Numeric(18, 2)))
INSERT [dbo].[Factura_Detalle] ([ID_Detalle], [ID_Parametro], [ID_IN_RE], [Descripcion], [Cantidad], [Precio_unitario], [Subtotal_linea], [Impuesto_linea]) VALUES (2114, 2088, 1307, N'limonada', 1, CAST(14.70 AS Numeric(18, 2)), CAST(29.40 AS Numeric(18, 2)), CAST(4.41 AS Numeric(18, 2)))
INSERT [dbo].[Factura_Detalle] ([ID_Detalle], [ID_Parametro], [ID_IN_RE], [Descripcion], [Cantidad], [Precio_unitario], [Subtotal_linea], [Impuesto_linea]) VALUES (2115, 2089, 1304, N'Alitas BBQ', 1, CAST(5.69 AS Numeric(18, 2)), CAST(21.66 AS Numeric(18, 2)), CAST(3.25 AS Numeric(18, 2)))
INSERT [dbo].[Factura_Detalle] ([ID_Detalle], [ID_Parametro], [ID_IN_RE], [Descripcion], [Cantidad], [Precio_unitario], [Subtotal_linea], [Impuesto_linea]) VALUES (2116, 2089, 1307, N'limonada', 1, CAST(14.70 AS Numeric(18, 2)), CAST(29.40 AS Numeric(18, 2)), CAST(4.41 AS Numeric(18, 2)))
INSERT [dbo].[Factura_Detalle] ([ID_Detalle], [ID_Parametro], [ID_IN_RE], [Descripcion], [Cantidad], [Precio_unitario], [Subtotal_linea], [Impuesto_linea]) VALUES (2117, 2090, 1304, N'Alitas BBQ', 1, CAST(5.69 AS Numeric(18, 2)), CAST(21.66 AS Numeric(18, 2)), CAST(3.25 AS Numeric(18, 2)))
INSERT [dbo].[Factura_Detalle] ([ID_Detalle], [ID_Parametro], [ID_IN_RE], [Descripcion], [Cantidad], [Precio_unitario], [Subtotal_linea], [Impuesto_linea]) VALUES (2118, 2090, 1307, N'limonada', 1, CAST(14.70 AS Numeric(18, 2)), CAST(29.40 AS Numeric(18, 2)), CAST(4.41 AS Numeric(18, 2)))
INSERT [dbo].[Factura_Detalle] ([ID_Detalle], [ID_Parametro], [ID_IN_RE], [Descripcion], [Cantidad], [Precio_unitario], [Subtotal_linea], [Impuesto_linea]) VALUES (2119, 2091, 1304, N'Alitas BBQ', 1, CAST(5.69 AS Numeric(18, 2)), CAST(21.66 AS Numeric(18, 2)), CAST(3.25 AS Numeric(18, 2)))
INSERT [dbo].[Factura_Detalle] ([ID_Detalle], [ID_Parametro], [ID_IN_RE], [Descripcion], [Cantidad], [Precio_unitario], [Subtotal_linea], [Impuesto_linea]) VALUES (2120, 2091, 1307, N'limonada', 1, CAST(14.70 AS Numeric(18, 2)), CAST(29.40 AS Numeric(18, 2)), CAST(4.41 AS Numeric(18, 2)))
INSERT [dbo].[Factura_Detalle] ([ID_Detalle], [ID_Parametro], [ID_IN_RE], [Descripcion], [Cantidad], [Precio_unitario], [Subtotal_linea], [Impuesto_linea]) VALUES (2121, 2092, 1304, N'Alitas BBQ', 1, CAST(5.69 AS Numeric(18, 2)), CAST(21.66 AS Numeric(18, 2)), CAST(3.25 AS Numeric(18, 2)))
INSERT [dbo].[Factura_Detalle] ([ID_Detalle], [ID_Parametro], [ID_IN_RE], [Descripcion], [Cantidad], [Precio_unitario], [Subtotal_linea], [Impuesto_linea]) VALUES (2122, 2092, 1307, N'limonada', 1, CAST(14.70 AS Numeric(18, 2)), CAST(29.40 AS Numeric(18, 2)), CAST(4.41 AS Numeric(18, 2)))
INSERT [dbo].[Factura_Detalle] ([ID_Detalle], [ID_Parametro], [ID_IN_RE], [Descripcion], [Cantidad], [Precio_unitario], [Subtotal_linea], [Impuesto_linea]) VALUES (2123, 2093, 1304, N'Alitas BBQ', 1, CAST(5.69 AS Numeric(18, 2)), CAST(21.66 AS Numeric(18, 2)), CAST(3.25 AS Numeric(18, 2)))
INSERT [dbo].[Factura_Detalle] ([ID_Detalle], [ID_Parametro], [ID_IN_RE], [Descripcion], [Cantidad], [Precio_unitario], [Subtotal_linea], [Impuesto_linea]) VALUES (2124, 2093, 1307, N'limonada', 1, CAST(14.70 AS Numeric(18, 2)), CAST(29.40 AS Numeric(18, 2)), CAST(4.41 AS Numeric(18, 2)))
INSERT [dbo].[Factura_Detalle] ([ID_Detalle], [ID_Parametro], [ID_IN_RE], [Descripcion], [Cantidad], [Precio_unitario], [Subtotal_linea], [Impuesto_linea]) VALUES (2125, 2094, 1307, N'limonada', 1, CAST(14.70 AS Numeric(18, 2)), CAST(29.40 AS Numeric(18, 2)), CAST(4.41 AS Numeric(18, 2)))
SET IDENTITY_INSERT [dbo].[Factura_Detalle] OFF
GO
SET IDENTITY_INSERT [dbo].[Facturas] ON 

INSERT [dbo].[Facturas] ([ID_Parametro], [Numero_Factura], [Fecha_Emision], [ID_Empleado], [ID_Cai], [Subtotal], [Descuento], [Impuesto], [Total_a_pagar], [ID_Usuario_ClienteF], [ID_pago]) VALUES (2088, N'011-001-01-000216', CAST(N'2025-12-14T12:59:23.980' AS DateTime), 21, 4, 43.4000, 0.0000, 7.6600, 51.0600, 1, 1)
INSERT [dbo].[Facturas] ([ID_Parametro], [Numero_Factura], [Fecha_Emision], [ID_Empleado], [ID_Cai], [Subtotal], [Descuento], [Impuesto], [Total_a_pagar], [ID_Usuario_ClienteF], [ID_pago]) VALUES (2089, N'011-001-01-000217', CAST(N'2025-12-15T01:03:33.653' AS DateTime), 21, 4, 43.4000, 0.0000, 7.6600, 51.0600, 1, 2)
INSERT [dbo].[Facturas] ([ID_Parametro], [Numero_Factura], [Fecha_Emision], [ID_Empleado], [ID_Cai], [Subtotal], [Descuento], [Impuesto], [Total_a_pagar], [ID_Usuario_ClienteF], [ID_pago]) VALUES (2090, N'011-001-01-000218', CAST(N'2025-12-15T02:31:00.317' AS DateTime), 21, 4, 43.4000, 0.0000, 7.6600, 51.0600, 1, 3)
INSERT [dbo].[Facturas] ([ID_Parametro], [Numero_Factura], [Fecha_Emision], [ID_Empleado], [ID_Cai], [Subtotal], [Descuento], [Impuesto], [Total_a_pagar], [ID_Usuario_ClienteF], [ID_pago]) VALUES (2091, N'011-001-01-000219', CAST(N'2025-12-15T02:40:55.213' AS DateTime), 21, 4, 43.4000, 0.0000, 7.6600, 51.0600, 1, 4)
INSERT [dbo].[Facturas] ([ID_Parametro], [Numero_Factura], [Fecha_Emision], [ID_Empleado], [ID_Cai], [Subtotal], [Descuento], [Impuesto], [Total_a_pagar], [ID_Usuario_ClienteF], [ID_pago]) VALUES (2092, N'011-001-01-000220', CAST(N'2025-12-15T03:44:29.910' AS DateTime), 21, 4, 43.4000, 0.0000, 7.6600, 51.0600, 1, 5)
INSERT [dbo].[Facturas] ([ID_Parametro], [Numero_Factura], [Fecha_Emision], [ID_Empleado], [ID_Cai], [Subtotal], [Descuento], [Impuesto], [Total_a_pagar], [ID_Usuario_ClienteF], [ID_pago]) VALUES (2093, N'011-001-01-000221', CAST(N'2025-12-15T03:44:48.630' AS DateTime), 21, 4, 43.4000, 0.0000, 7.6600, 51.0600, 1, 6)
INSERT [dbo].[Facturas] ([ID_Parametro], [Numero_Factura], [Fecha_Emision], [ID_Empleado], [ID_Cai], [Subtotal], [Descuento], [Impuesto], [Total_a_pagar], [ID_Usuario_ClienteF], [ID_pago]) VALUES (2094, N'011-001-01-000222', CAST(N'2026-02-02T03:36:54.077' AS DateTime), 21, 4, 24.9900, 0.0000, 4.4100, 29.4000, 1, 7)
SET IDENTITY_INSERT [dbo].[Facturas] OFF
GO
SET IDENTITY_INSERT [dbo].[Gerentes] ON 

INSERT [dbo].[Gerentes] ([ID_gerente], [Username], [Password], [ID_sucursal]) VALUES (1, N'gerente1', N'1234', 1)
SET IDENTITY_INSERT [dbo].[Gerentes] OFF
GO
SET IDENTITY_INSERT [dbo].[historial_ordenes_repartidor] ON 

INSERT [dbo].[historial_ordenes_repartidor] ([ID_Historial], [ID_Orden], [ID_Repartidor], [Estado_Final], [Fecha_Finalizacion], [Observacion]) VALUES (1, 10, 19, 3, CAST(N'2025-12-12T23:53:30.0000000' AS DateTime2), NULL)
INSERT [dbo].[historial_ordenes_repartidor] ([ID_Historial], [ID_Orden], [ID_Repartidor], [Estado_Final], [Fecha_Finalizacion], [Observacion]) VALUES (2, 16, 19, 3, CAST(N'2025-12-14T00:04:04.0000000' AS DateTime2), NULL)
INSERT [dbo].[historial_ordenes_repartidor] ([ID_Historial], [ID_Orden], [ID_Repartidor], [Estado_Final], [Fecha_Finalizacion], [Observacion]) VALUES (3, 15, 19, 3, CAST(N'2025-12-14T00:11:14.0000000' AS DateTime2), NULL)
INSERT [dbo].[historial_ordenes_repartidor] ([ID_Historial], [ID_Orden], [ID_Repartidor], [Estado_Final], [Fecha_Finalizacion], [Observacion]) VALUES (4, 14, 19, 3, CAST(N'2025-12-14T00:19:33.0000000' AS DateTime2), NULL)
INSERT [dbo].[historial_ordenes_repartidor] ([ID_Historial], [ID_Orden], [ID_Repartidor], [Estado_Final], [Fecha_Finalizacion], [Observacion]) VALUES (5, 13, 19, 3, CAST(N'2025-12-14T00:19:42.0000000' AS DateTime2), NULL)
INSERT [dbo].[historial_ordenes_repartidor] ([ID_Historial], [ID_Orden], [ID_Repartidor], [Estado_Final], [Fecha_Finalizacion], [Observacion]) VALUES (6, 12, 19, 3, CAST(N'2025-12-14T00:19:50.0000000' AS DateTime2), NULL)
INSERT [dbo].[historial_ordenes_repartidor] ([ID_Historial], [ID_Orden], [ID_Repartidor], [Estado_Final], [Fecha_Finalizacion], [Observacion]) VALUES (8, 18, 19, 4, CAST(N'2025-12-14T01:10:50.0000000' AS DateTime2), N'Cancelado por el cliente')
INSERT [dbo].[historial_ordenes_repartidor] ([ID_Historial], [ID_Orden], [ID_Repartidor], [Estado_Final], [Fecha_Finalizacion], [Observacion]) VALUES (9, 19, 19, 4, CAST(N'2025-12-14T01:11:43.0000000' AS DateTime2), N'Cancelado por el cliente')
INSERT [dbo].[historial_ordenes_repartidor] ([ID_Historial], [ID_Orden], [ID_Repartidor], [Estado_Final], [Fecha_Finalizacion], [Observacion]) VALUES (10, 20, 19, 4, CAST(N'2025-12-14T01:12:11.0000000' AS DateTime2), N'Cancelado por el cliente')
INSERT [dbo].[historial_ordenes_repartidor] ([ID_Historial], [ID_Orden], [ID_Repartidor], [Estado_Final], [Fecha_Finalizacion], [Observacion]) VALUES (11, 21, 19, 4, CAST(N'2025-12-14T01:15:36.0000000' AS DateTime2), N'ya no quiero no tengo hambre')
INSERT [dbo].[historial_ordenes_repartidor] ([ID_Historial], [ID_Orden], [ID_Repartidor], [Estado_Final], [Fecha_Finalizacion], [Observacion]) VALUES (1008, 2018, 19, 3, CAST(N'2025-12-14T14:56:40.0000000' AS DateTime2), NULL)
INSERT [dbo].[historial_ordenes_repartidor] ([ID_Historial], [ID_Orden], [ID_Repartidor], [Estado_Final], [Fecha_Finalizacion], [Observacion]) VALUES (1009, 2023, 19, 3, CAST(N'2025-12-15T03:47:12.0000000' AS DateTime2), NULL)
SET IDENTITY_INSERT [dbo].[historial_ordenes_repartidor] OFF
GO
SET IDENTITY_INSERT [dbo].[Impuesto_Categoria] ON 

INSERT [dbo].[Impuesto_Categoria] ([ID_Impuesto_Categoria], [ID_Impuesto], [ID_Categoria], [Activo]) VALUES (1, 2, 72, 1)
INSERT [dbo].[Impuesto_Categoria] ([ID_Impuesto_Categoria], [ID_Impuesto], [ID_Categoria], [Activo]) VALUES (3, 4, 1, 1)
INSERT [dbo].[Impuesto_Categoria] ([ID_Impuesto_Categoria], [ID_Impuesto], [ID_Categoria], [Activo]) VALUES (4, 4, 2, 1)
INSERT [dbo].[Impuesto_Categoria] ([ID_Impuesto_Categoria], [ID_Impuesto], [ID_Categoria], [Activo]) VALUES (5, 4, 3, 1)
INSERT [dbo].[Impuesto_Categoria] ([ID_Impuesto_Categoria], [ID_Impuesto], [ID_Categoria], [Activo]) VALUES (6, 4, 7, 1)
INSERT [dbo].[Impuesto_Categoria] ([ID_Impuesto_Categoria], [ID_Impuesto], [ID_Categoria], [Activo]) VALUES (7, 4, 8, 1)
INSERT [dbo].[Impuesto_Categoria] ([ID_Impuesto_Categoria], [ID_Impuesto], [ID_Categoria], [Activo]) VALUES (8, 4, 10, 1)
INSERT [dbo].[Impuesto_Categoria] ([ID_Impuesto_Categoria], [ID_Impuesto], [ID_Categoria], [Activo]) VALUES (9, 4, 12, 1)
INSERT [dbo].[Impuesto_Categoria] ([ID_Impuesto_Categoria], [ID_Impuesto], [ID_Categoria], [Activo]) VALUES (10, 4, 13, 1)
INSERT [dbo].[Impuesto_Categoria] ([ID_Impuesto_Categoria], [ID_Impuesto], [ID_Categoria], [Activo]) VALUES (11, 4, 14, 1)
INSERT [dbo].[Impuesto_Categoria] ([ID_Impuesto_Categoria], [ID_Impuesto], [ID_Categoria], [Activo]) VALUES (12, 4, 16, 1)
SET IDENTITY_INSERT [dbo].[Impuesto_Categoria] OFF
GO
SET IDENTITY_INSERT [dbo].[Impuesto_tasa_historica] ON 

INSERT [dbo].[Impuesto_tasa_historica] ([ID_Impuesto_historico], [ID_Impuesto], [fecha_inicio], [fecha_fin], [tasa]) VALUES (3, 2, CAST(N'2025-11-26T05:12:15.257' AS DateTime), CAST(N'2025-11-26T05:12:27.990' AS DateTime), CAST(17.00 AS Numeric(10, 2)))
INSERT [dbo].[Impuesto_tasa_historica] ([ID_Impuesto_historico], [ID_Impuesto], [fecha_inicio], [fecha_fin], [tasa]) VALUES (4, 2, CAST(N'2025-11-26T05:12:27.990' AS DateTime), CAST(N'2025-11-26T21:26:22.423' AS DateTime), CAST(18.00 AS Numeric(10, 2)))
INSERT [dbo].[Impuesto_tasa_historica] ([ID_Impuesto_historico], [ID_Impuesto], [fecha_inicio], [fecha_fin], [tasa]) VALUES (5, 2, CAST(N'2025-11-26T21:26:22.427' AS DateTime), CAST(N'2025-11-26T21:29:24.710' AS DateTime), CAST(16.00 AS Numeric(10, 2)))
INSERT [dbo].[Impuesto_tasa_historica] ([ID_Impuesto_historico], [ID_Impuesto], [fecha_inicio], [fecha_fin], [tasa]) VALUES (6, 2, CAST(N'2025-11-26T21:29:24.710' AS DateTime), NULL, CAST(18.00 AS Numeric(10, 2)))
INSERT [dbo].[Impuesto_tasa_historica] ([ID_Impuesto_historico], [ID_Impuesto], [fecha_inicio], [fecha_fin], [tasa]) VALUES (7, 4, CAST(N'2025-12-02T15:12:18.633' AS DateTime), CAST(N'2025-12-02T20:47:56.490' AS DateTime), CAST(15.00 AS Numeric(10, 2)))
INSERT [dbo].[Impuesto_tasa_historica] ([ID_Impuesto_historico], [ID_Impuesto], [fecha_inicio], [fecha_fin], [tasa]) VALUES (8, 4, CAST(N'2025-12-02T20:47:56.490' AS DateTime), CAST(N'2025-12-02T20:48:21.093' AS DateTime), CAST(16.00 AS Numeric(10, 2)))
INSERT [dbo].[Impuesto_tasa_historica] ([ID_Impuesto_historico], [ID_Impuesto], [fecha_inicio], [fecha_fin], [tasa]) VALUES (9, 4, CAST(N'2025-12-02T20:48:21.093' AS DateTime), NULL, CAST(15.00 AS Numeric(10, 2)))
SET IDENTITY_INSERT [dbo].[Impuesto_tasa_historica] OFF
GO
SET IDENTITY_INSERT [dbo].[Impuestos] ON 

INSERT [dbo].[Impuestos] ([ID_Impuesto], [Nombre_Impuesto], [tasa], [descripcion], [activo], [ID_Categoria]) VALUES (2, N'Bebidas Alcoholicass', CAST(18.00 AS Decimal(10, 2)), N'bebidas que contienen alcohol', 1, 72)
INSERT [dbo].[Impuestos] ([ID_Impuesto], [Nombre_Impuesto], [tasa], [descripcion], [activo], [ID_Categoria]) VALUES (4, N'Isv Quince', CAST(15.00 AS Decimal(10, 2)), N'insumos del 15%', 1, 1)
SET IDENTITY_INSERT [dbo].[Impuestos] OFF
GO
SET IDENTITY_INSERT [dbo].[IN_RE] ON 

INSERT [dbo].[IN_RE] ([ID_IN_RE], [Activo], [ID_Insumo], [ID_Receta], [cantidad_usada], [precio_final], [ID_Unidad], [ID_sucursal]) VALUES (1296, 1, 50, 2104, CAST(0.02 AS Decimal(10, 2)), 0.6000, 3, 11)
INSERT [dbo].[IN_RE] ([ID_IN_RE], [Activo], [ID_Insumo], [ID_Receta], [cantidad_usada], [precio_final], [ID_Unidad], [ID_sucursal]) VALUES (1297, 1, 43, 2104, CAST(0.22 AS Decimal(10, 2)), 37.9500, 3, 11)
INSERT [dbo].[IN_RE] ([ID_IN_RE], [Activo], [ID_Insumo], [ID_Receta], [cantidad_usada], [precio_final], [ID_Unidad], [ID_sucursal]) VALUES (1298, 1, 22, 2104, CAST(0.01 AS Decimal(10, 2)), 0.5200, 6, 11)
INSERT [dbo].[IN_RE] ([ID_IN_RE], [Activo], [ID_Insumo], [ID_Receta], [cantidad_usada], [precio_final], [ID_Unidad], [ID_sucursal]) VALUES (1299, 1, 50, 2105, CAST(0.20 AS Decimal(10, 2)), 6.0000, 3, 11)
INSERT [dbo].[IN_RE] ([ID_IN_RE], [Activo], [ID_Insumo], [ID_Receta], [cantidad_usada], [precio_final], [ID_Unidad], [ID_sucursal]) VALUES (1300, 1, 136, 2106, CAST(0.10 AS Decimal(10, 2)), 1.7300, 1, 11)
INSERT [dbo].[IN_RE] ([ID_IN_RE], [Activo], [ID_Insumo], [ID_Receta], [cantidad_usada], [precio_final], [ID_Unidad], [ID_sucursal]) VALUES (1301, 1, 50, 2106, CAST(0.01 AS Decimal(10, 2)), 0.3000, 3, 11)
INSERT [dbo].[IN_RE] ([ID_IN_RE], [Activo], [ID_Insumo], [ID_Receta], [cantidad_usada], [precio_final], [ID_Unidad], [ID_sucursal]) VALUES (1302, 1, 10, 2105, CAST(0.02 AS Decimal(10, 2)), 0.7000, 3, 11)
INSERT [dbo].[IN_RE] ([ID_IN_RE], [Activo], [ID_Insumo], [ID_Receta], [cantidad_usada], [precio_final], [ID_Unidad], [ID_sucursal]) VALUES (1303, 1, 137, 2107, CAST(50.00 AS Decimal(10, 2)), 86.0000, 2, 11)
INSERT [dbo].[IN_RE] ([ID_IN_RE], [Activo], [ID_Insumo], [ID_Receta], [cantidad_usada], [precio_final], [ID_Unidad], [ID_sucursal]) VALUES (1304, 1, 22, 2108, CAST(0.11 AS Decimal(10, 2)), 5.6925, 6, 11)
INSERT [dbo].[IN_RE] ([ID_IN_RE], [Activo], [ID_Insumo], [ID_Receta], [cantidad_usada], [precio_final], [ID_Unidad], [ID_sucursal]) VALUES (1305, 1, 13, 2108, CAST(0.22 AS Decimal(10, 2)), 1.2650, 1, 11)
INSERT [dbo].[IN_RE] ([ID_IN_RE], [Activo], [ID_Insumo], [ID_Receta], [cantidad_usada], [precio_final], [ID_Unidad], [ID_sucursal]) VALUES (1306, 1, 50, 2108, CAST(0.49 AS Decimal(10, 2)), 14.7000, 3, 11)
INSERT [dbo].[IN_RE] ([ID_IN_RE], [Activo], [ID_Insumo], [ID_Receta], [cantidad_usada], [precio_final], [ID_Unidad], [ID_sucursal]) VALUES (1307, 1, 50, 2109, CAST(0.49 AS Decimal(10, 2)), 14.7000, 3, 11)
INSERT [dbo].[IN_RE] ([ID_IN_RE], [Activo], [ID_Insumo], [ID_Receta], [cantidad_usada], [precio_final], [ID_Unidad], [ID_sucursal]) VALUES (1308, 1, 9, 2109, CAST(0.49 AS Decimal(10, 2)), 14.7000, 3, 11)
INSERT [dbo].[IN_RE] ([ID_IN_RE], [Activo], [ID_Insumo], [ID_Receta], [cantidad_usada], [precio_final], [ID_Unidad], [ID_sucursal]) VALUES (1309, 1, 39, 2110, CAST(0.11 AS Decimal(10, 2)), 8.8550, 6, 11)
INSERT [dbo].[IN_RE] ([ID_IN_RE], [Activo], [ID_Insumo], [ID_Receta], [cantidad_usada], [precio_final], [ID_Unidad], [ID_sucursal]) VALUES (1310, 1, 5, 2110, CAST(0.24 AS Decimal(10, 2)), 3.6000, 3, 11)
SET IDENTITY_INSERT [dbo].[IN_RE] OFF
GO
SET IDENTITY_INSERT [dbo].[Insumo_Precio_historico] ON 

INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (44, 43, CAST(N'2025-11-22' AS Date), CAST(N'2025-11-22T18:08:04.073' AS DateTime), CAST(180 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (45, 43, CAST(N'2025-11-22' AS Date), CAST(N'2025-11-22T19:54:15.443' AS DateTime), CAST(190 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (46, 51, CAST(N'2025-11-22' AS Date), NULL, CAST(10 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (47, 43, CAST(N'2025-11-22' AS Date), CAST(N'2025-11-22T19:54:59.643' AS DateTime), CAST(150 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (48, 43, CAST(N'2025-11-22' AS Date), CAST(N'2025-11-22T20:02:57.270' AS DateTime), CAST(100 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (49, 43, CAST(N'2025-11-22' AS Date), CAST(N'2025-11-22T20:04:24.247' AS DateTime), CAST(150 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (50, 43, CAST(N'2025-11-22' AS Date), CAST(N'2025-11-22T20:39:38.283' AS DateTime), CAST(100 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (51, 43, CAST(N'2025-11-22' AS Date), CAST(N'2025-11-22T20:40:31.747' AS DateTime), CAST(180 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (52, 43, CAST(N'2025-11-22' AS Date), CAST(N'2025-11-22T21:16:49.037' AS DateTime), CAST(110 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (53, 52, CAST(N'2025-11-22' AS Date), NULL, CAST(20 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (54, 81, CAST(N'2025-11-22' AS Date), CAST(N'2025-12-02T16:46:45.997' AS DateTime), CAST(15 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (55, 50, CAST(N'2025-11-22' AS Date), CAST(N'2025-11-23T08:40:28.763' AS DateTime), CAST(10 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (56, 43, CAST(N'2025-11-22' AS Date), CAST(N'2025-11-22T21:46:37.837' AS DateTime), CAST(180 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (57, 43, CAST(N'2025-11-22' AS Date), CAST(N'2025-11-22T21:47:22.857' AS DateTime), CAST(120 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (58, 43, CAST(N'2025-11-22' AS Date), CAST(N'2025-11-23T08:51:51.650' AS DateTime), CAST(180 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1051, 131, CAST(N'2025-11-23' AS Date), CAST(N'2025-11-28T08:45:59.330' AS DateTime), CAST(1 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1052, 50, CAST(N'2025-11-23' AS Date), NULL, CAST(30 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1053, 43, CAST(N'2025-11-23' AS Date), CAST(N'2025-11-23T08:53:22.970' AS DateTime), CAST(150 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1054, 43, CAST(N'2025-11-23' AS Date), CAST(N'2025-11-23T09:25:31.310' AS DateTime), CAST(10 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1055, 132, CAST(N'2025-11-23' AS Date), CAST(N'2025-12-02T16:46:46.000' AS DateTime), CAST(1 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1056, 43, CAST(N'2025-11-23' AS Date), CAST(N'2025-12-02T16:46:45.980' AS DateTime), CAST(150 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1057, 131, CAST(N'2025-11-28' AS Date), CAST(N'2025-12-02T16:46:46.000' AS DateTime), CAST(2 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1058, 4, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T20:47:56.507' AS DateTime), CAST(92 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1059, 12, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T20:47:56.510' AS DateTime), CAST(40 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1060, 13, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T20:47:56.510' AS DateTime), CAST(6 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1061, 14, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T20:47:56.513' AS DateTime), CAST(81 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1062, 15, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T20:47:56.513' AS DateTime), CAST(17 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1063, 16, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T20:47:56.517' AS DateTime), CAST(46 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1064, 17, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T20:47:56.517' AS DateTime), CAST(57 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1065, 18, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T20:47:56.520' AS DateTime), CAST(52 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1066, 20, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T20:47:56.520' AS DateTime), CAST(69 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1067, 22, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T20:47:56.520' AS DateTime), CAST(52 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1068, 23, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T20:47:56.523' AS DateTime), CAST(46 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1069, 24, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T20:47:56.523' AS DateTime), CAST(103 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1070, 32, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T20:47:56.523' AS DateTime), CAST(40 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1071, 33, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T20:47:56.527' AS DateTime), CAST(6 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1072, 34, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T20:47:56.527' AS DateTime), CAST(81 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1073, 35, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T20:47:56.527' AS DateTime), CAST(17 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1074, 36, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T20:47:56.530' AS DateTime), CAST(46 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1075, 37, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T20:47:56.530' AS DateTime), CAST(57 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1076, 38, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T20:47:56.530' AS DateTime), CAST(52 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1077, 39, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T20:47:56.533' AS DateTime), CAST(81 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1078, 40, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T20:47:56.533' AS DateTime), CAST(69 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1079, 41, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T20:47:56.533' AS DateTime), CAST(115 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1080, 42, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T20:47:56.537' AS DateTime), CAST(138 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1081, 43, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T20:47:56.537' AS DateTime), CAST(173 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1082, 44, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T20:47:56.537' AS DateTime), CAST(52 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1083, 45, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T20:47:56.540' AS DateTime), CAST(46 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1084, 46, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T20:47:56.540' AS DateTime), CAST(103 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1085, 55, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T20:47:56.543' AS DateTime), CAST(40 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1086, 56, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T20:47:56.543' AS DateTime), CAST(6 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1087, 57, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T20:47:56.543' AS DateTime), CAST(81 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1088, 58, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T20:47:56.547' AS DateTime), CAST(17 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1089, 59, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T20:47:56.547' AS DateTime), CAST(46 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1090, 60, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T20:47:56.547' AS DateTime), CAST(57 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1091, 61, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T20:47:56.550' AS DateTime), CAST(52 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1092, 62, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T20:47:56.550' AS DateTime), CAST(81 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1093, 63, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T20:47:56.550' AS DateTime), CAST(69 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1094, 81, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T20:47:56.550' AS DateTime), CAST(17 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1095, 121, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T20:47:56.553' AS DateTime), CAST(1 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1096, 122, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T20:47:56.553' AS DateTime), CAST(1 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1097, 131, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T20:47:56.553' AS DateTime), CAST(2 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1098, 132, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T20:47:56.557' AS DateTime), CAST(1 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1099, 135, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T20:47:56.557' AS DateTime), CAST(15 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1100, 136, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T17:25:28.957' AS DateTime), CAST(17 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1101, 136, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T17:26:46.837' AS DateTime), CAST(29 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1102, 136, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T20:46:59.347' AS DateTime), CAST(17 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1103, 136, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T20:47:56.557' AS DateTime), CAST(18 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1104, 4, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T20:48:21.100' AS DateTime), CAST(93 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1105, 12, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T20:48:21.103' AS DateTime), CAST(41 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1106, 13, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T20:48:21.107' AS DateTime), CAST(6 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1107, 14, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T20:48:21.107' AS DateTime), CAST(81 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1108, 15, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T20:48:21.110' AS DateTime), CAST(17 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1109, 16, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T20:48:21.110' AS DateTime), CAST(46 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1110, 17, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T20:48:21.110' AS DateTime), CAST(58 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1111, 18, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T20:48:21.113' AS DateTime), CAST(52 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1112, 20, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T20:48:21.113' AS DateTime), CAST(70 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1113, 22, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T20:48:21.113' AS DateTime), CAST(52 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1114, 23, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T20:48:21.117' AS DateTime), CAST(46 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1115, 24, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T20:48:21.117' AS DateTime), CAST(104 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1116, 32, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T20:48:21.120' AS DateTime), CAST(41 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1117, 33, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T20:48:21.120' AS DateTime), CAST(6 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1118, 34, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T20:48:21.120' AS DateTime), CAST(81 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1119, 35, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T20:48:21.123' AS DateTime), CAST(17 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1120, 36, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T20:48:21.123' AS DateTime), CAST(46 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1121, 37, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T20:48:21.123' AS DateTime), CAST(58 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1122, 38, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T20:48:21.127' AS DateTime), CAST(52 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1123, 39, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T20:48:21.127' AS DateTime), CAST(81 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1124, 40, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T20:48:21.127' AS DateTime), CAST(70 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1125, 41, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T20:48:21.130' AS DateTime), CAST(116 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1126, 42, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T20:48:21.130' AS DateTime), CAST(139 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1127, 43, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T20:48:21.130' AS DateTime), CAST(174 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1128, 44, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T20:48:21.130' AS DateTime), CAST(52 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1129, 45, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T20:48:21.133' AS DateTime), CAST(46 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1130, 46, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T20:48:21.133' AS DateTime), CAST(104 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1131, 55, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T20:48:21.133' AS DateTime), CAST(41 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1132, 56, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T20:48:21.137' AS DateTime), CAST(6 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1133, 57, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T20:48:21.137' AS DateTime), CAST(81 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1134, 58, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T20:48:21.137' AS DateTime), CAST(17 AS Decimal(18, 0)))
GO
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1135, 59, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T20:48:21.140' AS DateTime), CAST(46 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1136, 60, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T20:48:21.140' AS DateTime), CAST(58 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1137, 61, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T20:48:21.140' AS DateTime), CAST(52 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1138, 62, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T20:48:21.143' AS DateTime), CAST(81 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1139, 63, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T20:48:21.143' AS DateTime), CAST(70 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1140, 81, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T20:48:21.143' AS DateTime), CAST(17 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1141, 121, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T20:48:21.147' AS DateTime), CAST(1 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1142, 122, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T20:48:21.147' AS DateTime), CAST(1 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1143, 131, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T20:48:21.147' AS DateTime), CAST(2 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1144, 132, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T20:48:21.150' AS DateTime), CAST(1 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1145, 135, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T20:48:21.150' AS DateTime), CAST(17 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1146, 136, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T20:48:21.150' AS DateTime), CAST(19 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1147, 4, CAST(N'2025-12-02' AS Date), NULL, CAST(92 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1148, 12, CAST(N'2025-12-02' AS Date), NULL, CAST(40 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1149, 13, CAST(N'2025-12-02' AS Date), NULL, CAST(6 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1150, 14, CAST(N'2025-12-02' AS Date), NULL, CAST(81 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1151, 15, CAST(N'2025-12-02' AS Date), NULL, CAST(17 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1152, 16, CAST(N'2025-12-02' AS Date), NULL, CAST(46 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1153, 17, CAST(N'2025-12-02' AS Date), NULL, CAST(57 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1154, 18, CAST(N'2025-12-02' AS Date), NULL, CAST(52 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1155, 20, CAST(N'2025-12-02' AS Date), NULL, CAST(69 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1156, 22, CAST(N'2025-12-02' AS Date), NULL, CAST(52 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1157, 23, CAST(N'2025-12-02' AS Date), NULL, CAST(46 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1158, 24, CAST(N'2025-12-02' AS Date), NULL, CAST(103 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1159, 32, CAST(N'2025-12-02' AS Date), NULL, CAST(40 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1160, 33, CAST(N'2025-12-02' AS Date), NULL, CAST(6 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1161, 34, CAST(N'2025-12-02' AS Date), NULL, CAST(81 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1162, 35, CAST(N'2025-12-02' AS Date), NULL, CAST(17 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1163, 36, CAST(N'2025-12-02' AS Date), NULL, CAST(46 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1164, 37, CAST(N'2025-12-02' AS Date), NULL, CAST(57 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1165, 38, CAST(N'2025-12-02' AS Date), NULL, CAST(52 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1166, 39, CAST(N'2025-12-02' AS Date), NULL, CAST(81 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1167, 40, CAST(N'2025-12-02' AS Date), NULL, CAST(69 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1168, 41, CAST(N'2025-12-02' AS Date), NULL, CAST(115 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1169, 42, CAST(N'2025-12-02' AS Date), NULL, CAST(138 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1170, 43, CAST(N'2025-12-02' AS Date), NULL, CAST(173 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1171, 44, CAST(N'2025-12-02' AS Date), NULL, CAST(52 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1172, 45, CAST(N'2025-12-02' AS Date), NULL, CAST(46 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1173, 46, CAST(N'2025-12-02' AS Date), NULL, CAST(103 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1174, 55, CAST(N'2025-12-02' AS Date), NULL, CAST(40 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1175, 56, CAST(N'2025-12-02' AS Date), NULL, CAST(6 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1176, 57, CAST(N'2025-12-02' AS Date), NULL, CAST(81 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1177, 58, CAST(N'2025-12-02' AS Date), NULL, CAST(17 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1178, 59, CAST(N'2025-12-02' AS Date), NULL, CAST(46 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1179, 60, CAST(N'2025-12-02' AS Date), NULL, CAST(57 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1180, 61, CAST(N'2025-12-02' AS Date), NULL, CAST(52 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1181, 62, CAST(N'2025-12-02' AS Date), NULL, CAST(81 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1182, 63, CAST(N'2025-12-02' AS Date), NULL, CAST(69 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1183, 81, CAST(N'2025-12-02' AS Date), NULL, CAST(17 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1184, 121, CAST(N'2025-12-02' AS Date), NULL, CAST(1 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1185, 122, CAST(N'2025-12-02' AS Date), NULL, CAST(1 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1186, 131, CAST(N'2025-12-02' AS Date), NULL, CAST(2 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1187, 132, CAST(N'2025-12-02' AS Date), NULL, CAST(1 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1188, 135, CAST(N'2025-12-02' AS Date), NULL, CAST(17 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1189, 136, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T21:03:35.053' AS DateTime), CAST(18 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1190, 136, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T21:04:00.637' AS DateTime), CAST(1 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1191, 136, CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02T21:48:18.713' AS DateTime), CAST(0 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1192, 136, CAST(N'2025-12-02' AS Date), NULL, CAST(17 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1193, 137, CAST(N'2025-12-03' AS Date), NULL, CAST(2 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (1194, 138, CAST(N'2025-12-14' AS Date), NULL, CAST(25 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (2194, 1138, CAST(N'2025-12-14' AS Date), NULL, CAST(17 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (2195, 1139, CAST(N'2025-12-14' AS Date), NULL, CAST(17 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (2196, 1140, CAST(N'2026-01-12' AS Date), NULL, CAST(29 AS Decimal(18, 0)))
INSERT [dbo].[Insumo_Precio_historico] ([ID_Insumo_precio_historico], [ID_Insumo], [fecha_inicio], [fecha_fin], [Precio]) VALUES (2197, 1141, CAST(N'2026-02-02' AS Date), NULL, CAST(115 AS Decimal(18, 0)))
SET IDENTITY_INSERT [dbo].[Insumo_Precio_historico] OFF
GO
SET IDENTITY_INSERT [dbo].[Insumos] ON 

INSERT [dbo].[Insumos] ([ID_Insumo], [ID_Unidad], [Nombre_insumo], [stock_total], [stock_minimo], [precio_lempiras], [ID_Categoria], [peso_individual], [precio_base], [stock_maximo], [ID_sucursal]) VALUES (4, 6, N'aceite vegetal', 10, 3, CAST(92.00 AS Decimal(10, 2)), 16, CAST(1.00 AS Decimal(10, 2)), CAST(80.00 AS Decimal(18, 2)), NULL, 11)
INSERT [dbo].[Insumos] ([ID_Insumo], [ID_Unidad], [Nombre_insumo], [stock_total], [stock_minimo], [precio_lempiras], [ID_Categoria], [peso_individual], [precio_base], [stock_maximo], [ID_sucursal]) VALUES (5, 3, N'Sal', 229.2, 2, CAST(15.00 AS Decimal(10, 2)), 15, CAST(1.00 AS Decimal(10, 2)), CAST(15.00 AS Decimal(18, 2)), 200, 11)
INSERT [dbo].[Insumos] ([ID_Insumo], [ID_Unidad], [Nombre_insumo], [stock_total], [stock_minimo], [precio_lempiras], [ID_Categoria], [peso_individual], [precio_base], [stock_maximo], [ID_sucursal]) VALUES (6, 3, N'Pimienta negra', 28, 2, CAST(30.00 AS Decimal(10, 2)), 15, CAST(1.00 AS Decimal(10, 2)), CAST(30.00 AS Decimal(18, 2)), NULL, 11)
INSERT [dbo].[Insumos] ([ID_Insumo], [ID_Unidad], [Nombre_insumo], [stock_total], [stock_minimo], [precio_lempiras], [ID_Categoria], [peso_individual], [precio_base], [stock_maximo], [ID_sucursal]) VALUES (7, 3, N'Ajo en polvo', 5, 1, CAST(35.00 AS Decimal(10, 2)), 15, CAST(1.00 AS Decimal(10, 2)), CAST(35.00 AS Decimal(18, 2)), NULL, 11)
INSERT [dbo].[Insumos] ([ID_Insumo], [ID_Unidad], [Nombre_insumo], [stock_total], [stock_minimo], [precio_lempiras], [ID_Categoria], [peso_individual], [precio_base], [stock_maximo], [ID_sucursal]) VALUES (9, 3, N'Azúcar', 30, 10, CAST(30.00 AS Decimal(10, 2)), 9, CAST(1.00 AS Decimal(10, 2)), CAST(30.00 AS Decimal(18, 2)), NULL, 11)
INSERT [dbo].[Insumos] ([ID_Insumo], [ID_Unidad], [Nombre_insumo], [stock_total], [stock_minimo], [precio_lempiras], [ID_Categoria], [peso_individual], [precio_base], [stock_maximo], [ID_sucursal]) VALUES (10, 3, N'Harina', 30, 10, CAST(35.00 AS Decimal(10, 2)), 9, CAST(1.00 AS Decimal(10, 2)), CAST(35.00 AS Decimal(18, 2)), NULL, 11)
INSERT [dbo].[Insumos] ([ID_Insumo], [ID_Unidad], [Nombre_insumo], [stock_total], [stock_minimo], [precio_lempiras], [ID_Categoria], [peso_individual], [precio_base], [stock_maximo], [ID_sucursal]) VALUES (11, 3, N'Cacao en polvo', 15, 5, CAST(80.00 AS Decimal(10, 2)), 9, CAST(1.00 AS Decimal(10, 2)), CAST(80.00 AS Decimal(18, 2)), NULL, 11)
INSERT [dbo].[Insumos] ([ID_Insumo], [ID_Unidad], [Nombre_insumo], [stock_total], [stock_minimo], [precio_lempiras], [ID_Categoria], [peso_individual], [precio_base], [stock_maximo], [ID_sucursal]) VALUES (12, 6, N'Leche líquida', 25, 5, CAST(40.25 AS Decimal(10, 2)), 12, CAST(1.00 AS Decimal(10, 2)), CAST(35.00 AS Decimal(18, 2)), NULL, 11)
INSERT [dbo].[Insumos] ([ID_Insumo], [ID_Unidad], [Nombre_insumo], [stock_total], [stock_minimo], [precio_lempiras], [ID_Categoria], [peso_individual], [precio_base], [stock_maximo], [ID_sucursal]) VALUES (13, 1, N'Huevos', 10, 3, CAST(5.75 AS Decimal(10, 2)), 12, CAST(1.00 AS Decimal(10, 2)), CAST(5.00 AS Decimal(18, 2)), NULL, 11)
INSERT [dbo].[Insumos] ([ID_Insumo], [ID_Unidad], [Nombre_insumo], [stock_total], [stock_minimo], [precio_lempiras], [ID_Categoria], [peso_individual], [precio_base], [stock_maximo], [ID_sucursal]) VALUES (14, 2, N'Mantequilla', 8, 2, CAST(80.50 AS Decimal(10, 2)), 12, CAST(1.00 AS Decimal(10, 2)), CAST(70.00 AS Decimal(18, 2)), NULL, 11)
INSERT [dbo].[Insumos] ([ID_Insumo], [ID_Unidad], [Nombre_insumo], [stock_total], [stock_minimo], [precio_lempiras], [ID_Categoria], [peso_individual], [precio_base], [stock_maximo], [ID_sucursal]) VALUES (15, 6, N'Agua purificada', 40, 10, CAST(17.25 AS Decimal(10, 2)), 14, CAST(1.00 AS Decimal(10, 2)), CAST(15.00 AS Decimal(18, 2)), NULL, 11)
INSERT [dbo].[Insumos] ([ID_Insumo], [ID_Unidad], [Nombre_insumo], [stock_total], [stock_minimo], [precio_lempiras], [ID_Categoria], [peso_individual], [precio_base], [stock_maximo], [ID_sucursal]) VALUES (16, 6, N'Concentrado de jamaica', 10, 3, CAST(46.00 AS Decimal(10, 2)), 14, CAST(1.00 AS Decimal(10, 2)), CAST(40.00 AS Decimal(18, 2)), NULL, 11)
INSERT [dbo].[Insumos] ([ID_Insumo], [ID_Unidad], [Nombre_insumo], [stock_total], [stock_minimo], [precio_lempiras], [ID_Categoria], [peso_individual], [precio_base], [stock_maximo], [ID_sucursal]) VALUES (17, 6, N'Concentrado de horchata', 10, 3, CAST(57.50 AS Decimal(10, 2)), 14, CAST(1.00 AS Decimal(10, 2)), CAST(50.00 AS Decimal(18, 2)), NULL, 11)
INSERT [dbo].[Insumos] ([ID_Insumo], [ID_Unidad], [Nombre_insumo], [stock_total], [stock_minimo], [precio_lempiras], [ID_Categoria], [peso_individual], [precio_base], [stock_maximo], [ID_sucursal]) VALUES (18, 6, N'Jugo de limón concentrado', 15, 5, CAST(51.75 AS Decimal(10, 2)), 14, CAST(1.00 AS Decimal(10, 2)), CAST(45.00 AS Decimal(18, 2)), NULL, 11)
INSERT [dbo].[Insumos] ([ID_Insumo], [ID_Unidad], [Nombre_insumo], [stock_total], [stock_minimo], [precio_lempiras], [ID_Categoria], [peso_individual], [precio_base], [stock_maximo], [ID_sucursal]) VALUES (20, 6, N'Mostaza', 10, 2, CAST(69.00 AS Decimal(10, 2)), 13, CAST(1.00 AS Decimal(10, 2)), CAST(60.00 AS Decimal(18, 2)), NULL, 11)
INSERT [dbo].[Insumos] ([ID_Insumo], [ID_Unidad], [Nombre_insumo], [stock_total], [stock_minimo], [precio_lempiras], [ID_Categoria], [peso_individual], [precio_base], [stock_maximo], [ID_sucursal]) VALUES (22, 6, N'Salsa BBQ', 18.9, 5, CAST(51.75 AS Decimal(10, 2)), 8, CAST(1.00 AS Decimal(10, 2)), CAST(45.00 AS Decimal(18, 2)), NULL, 11)
INSERT [dbo].[Insumos] ([ID_Insumo], [ID_Unidad], [Nombre_insumo], [stock_total], [stock_minimo], [precio_lempiras], [ID_Categoria], [peso_individual], [precio_base], [stock_maximo], [ID_sucursal]) VALUES (23, 6, N'Salsa Picante', 23, 4, CAST(46.00 AS Decimal(10, 2)), 8, CAST(1.00 AS Decimal(10, 2)), CAST(40.00 AS Decimal(18, 2)), NULL, 11)
INSERT [dbo].[Insumos] ([ID_Insumo], [ID_Unidad], [Nombre_insumo], [stock_total], [stock_minimo], [precio_lempiras], [ID_Categoria], [peso_individual], [precio_base], [stock_maximo], [ID_sucursal]) VALUES (24, 6, N'Aceite vegetal', 10, 3, CAST(103.50 AS Decimal(10, 2)), 16, CAST(1.00 AS Decimal(10, 2)), CAST(90.00 AS Decimal(18, 2)), NULL, 11)
INSERT [dbo].[Insumos] ([ID_Insumo], [ID_Unidad], [Nombre_insumo], [stock_total], [stock_minimo], [precio_lempiras], [ID_Categoria], [peso_individual], [precio_base], [stock_maximo], [ID_sucursal]) VALUES (26, 3, N'Pimienta negra', 8, 2, CAST(30.00 AS Decimal(10, 2)), 15, CAST(1.00 AS Decimal(10, 2)), CAST(30.00 AS Decimal(18, 2)), NULL, 11)
INSERT [dbo].[Insumos] ([ID_Insumo], [ID_Unidad], [Nombre_insumo], [stock_total], [stock_minimo], [precio_lempiras], [ID_Categoria], [peso_individual], [precio_base], [stock_maximo], [ID_sucursal]) VALUES (27, 3, N'Ajo en polvo', 5, 1, CAST(35.00 AS Decimal(10, 2)), 15, CAST(1.00 AS Decimal(10, 2)), CAST(35.00 AS Decimal(18, 2)), NULL, 11)
INSERT [dbo].[Insumos] ([ID_Insumo], [ID_Unidad], [Nombre_insumo], [stock_total], [stock_minimo], [precio_lempiras], [ID_Categoria], [peso_individual], [precio_base], [stock_maximo], [ID_sucursal]) VALUES (29, 3, N'Azúcar', 30, 10, CAST(30.00 AS Decimal(10, 2)), 9, CAST(1.00 AS Decimal(10, 2)), CAST(30.00 AS Decimal(18, 2)), NULL, 11)
INSERT [dbo].[Insumos] ([ID_Insumo], [ID_Unidad], [Nombre_insumo], [stock_total], [stock_minimo], [precio_lempiras], [ID_Categoria], [peso_individual], [precio_base], [stock_maximo], [ID_sucursal]) VALUES (30, 3, N'Harina', 30, 10, CAST(35.00 AS Decimal(10, 2)), 9, CAST(1.00 AS Decimal(10, 2)), CAST(35.00 AS Decimal(18, 2)), NULL, 11)
INSERT [dbo].[Insumos] ([ID_Insumo], [ID_Unidad], [Nombre_insumo], [stock_total], [stock_minimo], [precio_lempiras], [ID_Categoria], [peso_individual], [precio_base], [stock_maximo], [ID_sucursal]) VALUES (31, 3, N'Cacao en polvo', 15, 5, CAST(80.00 AS Decimal(10, 2)), 9, CAST(1.00 AS Decimal(10, 2)), CAST(80.00 AS Decimal(18, 2)), NULL, 11)
INSERT [dbo].[Insumos] ([ID_Insumo], [ID_Unidad], [Nombre_insumo], [stock_total], [stock_minimo], [precio_lempiras], [ID_Categoria], [peso_individual], [precio_base], [stock_maximo], [ID_sucursal]) VALUES (32, 6, N'Leche líquida', 25, 5, CAST(40.25 AS Decimal(10, 2)), 12, CAST(1.00 AS Decimal(10, 2)), CAST(35.00 AS Decimal(18, 2)), NULL, 11)
INSERT [dbo].[Insumos] ([ID_Insumo], [ID_Unidad], [Nombre_insumo], [stock_total], [stock_minimo], [precio_lempiras], [ID_Categoria], [peso_individual], [precio_base], [stock_maximo], [ID_sucursal]) VALUES (33, 1, N'Huevos', 10, 3, CAST(5.75 AS Decimal(10, 2)), 12, CAST(1.00 AS Decimal(10, 2)), CAST(5.00 AS Decimal(18, 2)), NULL, 11)
INSERT [dbo].[Insumos] ([ID_Insumo], [ID_Unidad], [Nombre_insumo], [stock_total], [stock_minimo], [precio_lempiras], [ID_Categoria], [peso_individual], [precio_base], [stock_maximo], [ID_sucursal]) VALUES (34, 2, N'Mantequilla', 8, 2, CAST(80.50 AS Decimal(10, 2)), 12, CAST(1.00 AS Decimal(10, 2)), CAST(70.00 AS Decimal(18, 2)), NULL, 11)
INSERT [dbo].[Insumos] ([ID_Insumo], [ID_Unidad], [Nombre_insumo], [stock_total], [stock_minimo], [precio_lempiras], [ID_Categoria], [peso_individual], [precio_base], [stock_maximo], [ID_sucursal]) VALUES (35, 6, N'Agua purificada', 40, 10, CAST(17.25 AS Decimal(10, 2)), 14, CAST(1.00 AS Decimal(10, 2)), CAST(15.00 AS Decimal(18, 2)), NULL, 11)
INSERT [dbo].[Insumos] ([ID_Insumo], [ID_Unidad], [Nombre_insumo], [stock_total], [stock_minimo], [precio_lempiras], [ID_Categoria], [peso_individual], [precio_base], [stock_maximo], [ID_sucursal]) VALUES (36, 6, N'Concentrado de jamaica', 10, 3, CAST(46.00 AS Decimal(10, 2)), 14, CAST(1.00 AS Decimal(10, 2)), CAST(40.00 AS Decimal(18, 2)), NULL, 11)
INSERT [dbo].[Insumos] ([ID_Insumo], [ID_Unidad], [Nombre_insumo], [stock_total], [stock_minimo], [precio_lempiras], [ID_Categoria], [peso_individual], [precio_base], [stock_maximo], [ID_sucursal]) VALUES (37, 6, N'Concentrado de horchata', 10, 3, CAST(57.50 AS Decimal(10, 2)), 14, CAST(1.00 AS Decimal(10, 2)), CAST(50.00 AS Decimal(18, 2)), NULL, 11)
INSERT [dbo].[Insumos] ([ID_Insumo], [ID_Unidad], [Nombre_insumo], [stock_total], [stock_minimo], [precio_lempiras], [ID_Categoria], [peso_individual], [precio_base], [stock_maximo], [ID_sucursal]) VALUES (38, 6, N'Jugo de limón concentrado', 15, 5, CAST(51.75 AS Decimal(10, 2)), 14, CAST(1.00 AS Decimal(10, 2)), CAST(45.00 AS Decimal(18, 2)), NULL, 11)
INSERT [dbo].[Insumos] ([ID_Insumo], [ID_Unidad], [Nombre_insumo], [stock_total], [stock_minimo], [precio_lempiras], [ID_Categoria], [peso_individual], [precio_base], [stock_maximo], [ID_sucursal]) VALUES (39, 6, N'Mayonesa', 11.78, 3, CAST(80.50 AS Decimal(10, 2)), 13, CAST(1.00 AS Decimal(10, 2)), CAST(70.00 AS Decimal(18, 2)), NULL, 11)
INSERT [dbo].[Insumos] ([ID_Insumo], [ID_Unidad], [Nombre_insumo], [stock_total], [stock_minimo], [precio_lempiras], [ID_Categoria], [peso_individual], [precio_base], [stock_maximo], [ID_sucursal]) VALUES (40, 6, N'Mostaza', 10, 2, CAST(69.00 AS Decimal(10, 2)), 13, CAST(1.00 AS Decimal(10, 2)), CAST(60.00 AS Decimal(18, 2)), NULL, 11)
INSERT [dbo].[Insumos] ([ID_Insumo], [ID_Unidad], [Nombre_insumo], [stock_total], [stock_minimo], [precio_lempiras], [ID_Categoria], [peso_individual], [precio_base], [stock_maximo], [ID_sucursal]) VALUES (41, 3, N'Alitas de pollo', 50, 10, CAST(115.00 AS Decimal(10, 2)), 2, CAST(1.00 AS Decimal(10, 2)), CAST(100.00 AS Decimal(18, 2)), NULL, 11)
INSERT [dbo].[Insumos] ([ID_Insumo], [ID_Unidad], [Nombre_insumo], [stock_total], [stock_minimo], [precio_lempiras], [ID_Categoria], [peso_individual], [precio_base], [stock_maximo], [ID_sucursal]) VALUES (42, 3, N'Pechuga de pollo', 30, 5, CAST(138.00 AS Decimal(10, 2)), 2, CAST(1.00 AS Decimal(10, 2)), CAST(120.00 AS Decimal(18, 2)), NULL, 11)
INSERT [dbo].[Insumos] ([ID_Insumo], [ID_Unidad], [Nombre_insumo], [stock_total], [stock_minimo], [precio_lempiras], [ID_Categoria], [peso_individual], [precio_base], [stock_maximo], [ID_sucursal]) VALUES (43, 3, N'Costillas BBQ', 10, 5, CAST(172.50 AS Decimal(10, 2)), 2, CAST(1.00 AS Decimal(10, 2)), CAST(150.00 AS Decimal(18, 2)), NULL, 11)
INSERT [dbo].[Insumos] ([ID_Insumo], [ID_Unidad], [Nombre_insumo], [stock_total], [stock_minimo], [precio_lempiras], [ID_Categoria], [peso_individual], [precio_base], [stock_maximo], [ID_sucursal]) VALUES (44, 6, N'Salsa BBQ', 10, 5, CAST(51.75 AS Decimal(10, 2)), 8, CAST(1.00 AS Decimal(10, 2)), CAST(45.00 AS Decimal(18, 2)), NULL, 11)
INSERT [dbo].[Insumos] ([ID_Insumo], [ID_Unidad], [Nombre_insumo], [stock_total], [stock_minimo], [precio_lempiras], [ID_Categoria], [peso_individual], [precio_base], [stock_maximo], [ID_sucursal]) VALUES (45, 6, N'Salsa Picante', 15, 4, CAST(46.00 AS Decimal(10, 2)), 8, CAST(1.00 AS Decimal(10, 2)), CAST(40.00 AS Decimal(18, 2)), NULL, 11)
INSERT [dbo].[Insumos] ([ID_Insumo], [ID_Unidad], [Nombre_insumo], [stock_total], [stock_minimo], [precio_lempiras], [ID_Categoria], [peso_individual], [precio_base], [stock_maximo], [ID_sucursal]) VALUES (46, 6, N'Aceite vegetal', 10, 3, CAST(103.50 AS Decimal(10, 2)), 16, CAST(1.00 AS Decimal(10, 2)), CAST(90.00 AS Decimal(18, 2)), NULL, 11)
INSERT [dbo].[Insumos] ([ID_Insumo], [ID_Unidad], [Nombre_insumo], [stock_total], [stock_minimo], [precio_lempiras], [ID_Categoria], [peso_individual], [precio_base], [stock_maximo], [ID_sucursal]) VALUES (48, 3, N'Pimienta negra', 8, 2, CAST(30.00 AS Decimal(10, 2)), 15, CAST(1.00 AS Decimal(10, 2)), CAST(30.00 AS Decimal(18, 2)), NULL, 11)
INSERT [dbo].[Insumos] ([ID_Insumo], [ID_Unidad], [Nombre_insumo], [stock_total], [stock_minimo], [precio_lempiras], [ID_Categoria], [peso_individual], [precio_base], [stock_maximo], [ID_sucursal]) VALUES (49, 3, N'Ajo en polvo', 5, 1, CAST(35.00 AS Decimal(10, 2)), 15, CAST(1.00 AS Decimal(10, 2)), CAST(35.00 AS Decimal(18, 2)), NULL, 11)
INSERT [dbo].[Insumos] ([ID_Insumo], [ID_Unidad], [Nombre_insumo], [stock_total], [stock_minimo], [precio_lempiras], [ID_Categoria], [peso_individual], [precio_base], [stock_maximo], [ID_sucursal]) VALUES (50, 3, N'Limón', 62.51, 10, CAST(30.00 AS Decimal(10, 2)), 6, CAST(1.00 AS Decimal(10, 2)), CAST(20.00 AS Decimal(18, 2)), NULL, 11)
INSERT [dbo].[Insumos] ([ID_Insumo], [ID_Unidad], [Nombre_insumo], [stock_total], [stock_minimo], [precio_lempiras], [ID_Categoria], [peso_individual], [precio_base], [stock_maximo], [ID_sucursal]) VALUES (51, 3, N'Manzana', 10, 5, CAST(10.00 AS Decimal(10, 2)), 6, CAST(1.00 AS Decimal(10, 2)), CAST(10.00 AS Decimal(18, 2)), NULL, 11)
INSERT [dbo].[Insumos] ([ID_Insumo], [ID_Unidad], [Nombre_insumo], [stock_total], [stock_minimo], [precio_lempiras], [ID_Categoria], [peso_individual], [precio_base], [stock_maximo], [ID_sucursal]) VALUES (52, 3, N'Azúcar', 30, 10, CAST(20.00 AS Decimal(10, 2)), 9, CAST(1.00 AS Decimal(10, 2)), CAST(20.00 AS Decimal(18, 2)), NULL, 11)
INSERT [dbo].[Insumos] ([ID_Insumo], [ID_Unidad], [Nombre_insumo], [stock_total], [stock_minimo], [precio_lempiras], [ID_Categoria], [peso_individual], [precio_base], [stock_maximo], [ID_sucursal]) VALUES (53, 3, N'Harina', 30, 10, CAST(35.00 AS Decimal(10, 2)), 9, CAST(1.00 AS Decimal(10, 2)), CAST(35.00 AS Decimal(18, 2)), NULL, 11)
INSERT [dbo].[Insumos] ([ID_Insumo], [ID_Unidad], [Nombre_insumo], [stock_total], [stock_minimo], [precio_lempiras], [ID_Categoria], [peso_individual], [precio_base], [stock_maximo], [ID_sucursal]) VALUES (54, 3, N'Cacao en polvo', 15, 5, CAST(80.00 AS Decimal(10, 2)), 9, CAST(1.00 AS Decimal(10, 2)), CAST(80.00 AS Decimal(18, 2)), NULL, 11)
INSERT [dbo].[Insumos] ([ID_Insumo], [ID_Unidad], [Nombre_insumo], [stock_total], [stock_minimo], [precio_lempiras], [ID_Categoria], [peso_individual], [precio_base], [stock_maximo], [ID_sucursal]) VALUES (55, 6, N'Leche líquida', 25, 5, CAST(40.25 AS Decimal(10, 2)), 12, CAST(1.00 AS Decimal(10, 2)), CAST(35.00 AS Decimal(18, 2)), NULL, 11)
INSERT [dbo].[Insumos] ([ID_Insumo], [ID_Unidad], [Nombre_insumo], [stock_total], [stock_minimo], [precio_lempiras], [ID_Categoria], [peso_individual], [precio_base], [stock_maximo], [ID_sucursal]) VALUES (56, 1, N'Huevos', 10, 3, CAST(5.75 AS Decimal(10, 2)), 12, CAST(1.00 AS Decimal(10, 2)), CAST(5.00 AS Decimal(18, 2)), NULL, 11)
INSERT [dbo].[Insumos] ([ID_Insumo], [ID_Unidad], [Nombre_insumo], [stock_total], [stock_minimo], [precio_lempiras], [ID_Categoria], [peso_individual], [precio_base], [stock_maximo], [ID_sucursal]) VALUES (57, 2, N'Mantequilla', 8, 2, CAST(80.50 AS Decimal(10, 2)), 12, CAST(1.00 AS Decimal(10, 2)), CAST(70.00 AS Decimal(18, 2)), NULL, 11)
INSERT [dbo].[Insumos] ([ID_Insumo], [ID_Unidad], [Nombre_insumo], [stock_total], [stock_minimo], [precio_lempiras], [ID_Categoria], [peso_individual], [precio_base], [stock_maximo], [ID_sucursal]) VALUES (58, 6, N'Agua purificada', 40, 10, CAST(17.25 AS Decimal(10, 2)), 14, CAST(1.00 AS Decimal(10, 2)), CAST(15.00 AS Decimal(18, 2)), NULL, 11)
INSERT [dbo].[Insumos] ([ID_Insumo], [ID_Unidad], [Nombre_insumo], [stock_total], [stock_minimo], [precio_lempiras], [ID_Categoria], [peso_individual], [precio_base], [stock_maximo], [ID_sucursal]) VALUES (59, 6, N'Concentrado de jamaica', 10, 3, CAST(46.00 AS Decimal(10, 2)), 14, CAST(1.00 AS Decimal(10, 2)), CAST(40.00 AS Decimal(18, 2)), NULL, 11)
INSERT [dbo].[Insumos] ([ID_Insumo], [ID_Unidad], [Nombre_insumo], [stock_total], [stock_minimo], [precio_lempiras], [ID_Categoria], [peso_individual], [precio_base], [stock_maximo], [ID_sucursal]) VALUES (60, 6, N'Concentrado de horchata', 10, 3, CAST(57.50 AS Decimal(10, 2)), 14, CAST(1.00 AS Decimal(10, 2)), CAST(50.00 AS Decimal(18, 2)), NULL, 11)
INSERT [dbo].[Insumos] ([ID_Insumo], [ID_Unidad], [Nombre_insumo], [stock_total], [stock_minimo], [precio_lempiras], [ID_Categoria], [peso_individual], [precio_base], [stock_maximo], [ID_sucursal]) VALUES (61, 6, N'Jugo de limón concentrado', 15, 5, CAST(51.75 AS Decimal(10, 2)), 14, CAST(1.00 AS Decimal(10, 2)), CAST(45.00 AS Decimal(18, 2)), NULL, 11)
INSERT [dbo].[Insumos] ([ID_Insumo], [ID_Unidad], [Nombre_insumo], [stock_total], [stock_minimo], [precio_lempiras], [ID_Categoria], [peso_individual], [precio_base], [stock_maximo], [ID_sucursal]) VALUES (62, 6, N'Mayonesa', 12, 3, CAST(80.50 AS Decimal(10, 2)), 13, CAST(1.00 AS Decimal(10, 2)), CAST(70.00 AS Decimal(18, 2)), NULL, 11)
INSERT [dbo].[Insumos] ([ID_Insumo], [ID_Unidad], [Nombre_insumo], [stock_total], [stock_minimo], [precio_lempiras], [ID_Categoria], [peso_individual], [precio_base], [stock_maximo], [ID_sucursal]) VALUES (63, 6, N'Mostaza', 10, 2, CAST(69.00 AS Decimal(10, 2)), 13, CAST(1.00 AS Decimal(10, 2)), CAST(60.00 AS Decimal(18, 2)), NULL, 11)
INSERT [dbo].[Insumos] ([ID_Insumo], [ID_Unidad], [Nombre_insumo], [stock_total], [stock_minimo], [precio_lempiras], [ID_Categoria], [peso_individual], [precio_base], [stock_maximo], [ID_sucursal]) VALUES (81, 1, N'Aceite', 22, 1, CAST(17.25 AS Decimal(10, 2)), 16, CAST(1.00 AS Decimal(10, 2)), CAST(15.00 AS Decimal(18, 2)), NULL, 11)
INSERT [dbo].[Insumos] ([ID_Insumo], [ID_Unidad], [Nombre_insumo], [stock_total], [stock_minimo], [precio_lempiras], [ID_Categoria], [peso_individual], [precio_base], [stock_maximo], [ID_sucursal]) VALUES (121, 2, N'Ejemplo ', 1, 1, CAST(1.15 AS Decimal(10, 2)), 13, CAST(1.00 AS Decimal(10, 2)), CAST(1.00 AS Decimal(18, 2)), NULL, 11)
INSERT [dbo].[Insumos] ([ID_Insumo], [ID_Unidad], [Nombre_insumo], [stock_total], [stock_minimo], [precio_lempiras], [ID_Categoria], [peso_individual], [precio_base], [stock_maximo], [ID_sucursal]) VALUES (122, 2, N'Ejemplo S', 1, 1, CAST(1.15 AS Decimal(10, 2)), 16, CAST(1.00 AS Decimal(10, 2)), CAST(1.00 AS Decimal(18, 2)), NULL, 11)
INSERT [dbo].[Insumos] ([ID_Insumo], [ID_Unidad], [Nombre_insumo], [stock_total], [stock_minimo], [precio_lempiras], [ID_Categoria], [peso_individual], [precio_base], [stock_maximo], [ID_sucursal]) VALUES (131, 2, N'Ejemplo 2', 7, 2, CAST(2.30 AS Decimal(10, 2)), 2, CAST(1.00 AS Decimal(10, 2)), CAST(2.00 AS Decimal(18, 2)), NULL, 11)
INSERT [dbo].[Insumos] ([ID_Insumo], [ID_Unidad], [Nombre_insumo], [stock_total], [stock_minimo], [precio_lempiras], [ID_Categoria], [peso_individual], [precio_base], [stock_maximo], [ID_sucursal]) VALUES (132, 2, N'Dsads', 1, 1, CAST(1.15 AS Decimal(10, 2)), 16, CAST(1.00 AS Decimal(10, 2)), CAST(1.00 AS Decimal(18, 2)), NULL, 11)
INSERT [dbo].[Insumos] ([ID_Insumo], [ID_Unidad], [Nombre_insumo], [stock_total], [stock_minimo], [precio_lempiras], [ID_Categoria], [peso_individual], [precio_base], [stock_maximo], [ID_sucursal]) VALUES (135, 3, N'Ejemplo Wes', 7, 2, CAST(17.25 AS Decimal(10, 2)), 2, CAST(1.00 AS Decimal(10, 2)), CAST(15.00 AS Decimal(18, 2)), NULL, 11)
INSERT [dbo].[Insumos] ([ID_Insumo], [ID_Unidad], [Nombre_insumo], [stock_total], [stock_minimo], [precio_lempiras], [ID_Categoria], [peso_individual], [precio_base], [stock_maximo], [ID_sucursal]) VALUES (136, 1, N'Ejemplo Qq', 0.04, 2, CAST(17.25 AS Decimal(10, 2)), 2, CAST(1.00 AS Decimal(10, 2)), CAST(15.00 AS Decimal(18, 2)), 200, 11)
INSERT [dbo].[Insumos] ([ID_Insumo], [ID_Unidad], [Nombre_insumo], [stock_total], [stock_minimo], [precio_lempiras], [ID_Categoria], [peso_individual], [precio_base], [stock_maximo], [ID_sucursal]) VALUES (137, 2, N'Ejemplo Zas', 300, 12, CAST(1.72 AS Decimal(10, 2)), 2, CAST(1.00 AS Decimal(10, 2)), CAST(1.50 AS Decimal(18, 2)), 1000, 11)
INSERT [dbo].[Insumos] ([ID_Insumo], [ID_Unidad], [Nombre_insumo], [stock_total], [stock_minimo], [precio_lempiras], [ID_Categoria], [peso_individual], [precio_base], [stock_maximo], [ID_sucursal]) VALUES (138, 3, N'Sal', 55, 10, CAST(25.00 AS Decimal(10, 2)), 15, CAST(1.00 AS Decimal(10, 2)), CAST(25.00 AS Decimal(18, 2)), 200, 1)
INSERT [dbo].[Insumos] ([ID_Insumo], [ID_Unidad], [Nombre_insumo], [stock_total], [stock_minimo], [precio_lempiras], [ID_Categoria], [peso_individual], [precio_base], [stock_maximo], [ID_sucursal]) VALUES (1138, 3, N'Pan', 166, 10, CAST(17.25 AS Decimal(10, 2)), 7, CAST(1.00 AS Decimal(10, 2)), CAST(15.00 AS Decimal(18, 2)), 300, 1)
INSERT [dbo].[Insumos] ([ID_Insumo], [ID_Unidad], [Nombre_insumo], [stock_total], [stock_minimo], [precio_lempiras], [ID_Categoria], [peso_individual], [precio_base], [stock_maximo], [ID_sucursal]) VALUES (1139, 6, N'Agua', 110, 2, CAST(17.25 AS Decimal(10, 2)), 14, CAST(1.00 AS Decimal(10, 2)), CAST(15.00 AS Decimal(18, 2)), 1000, 1)
INSERT [dbo].[Insumos] ([ID_Insumo], [ID_Unidad], [Nombre_insumo], [stock_total], [stock_minimo], [precio_lempiras], [ID_Categoria], [peso_individual], [precio_base], [stock_maximo], [ID_sucursal]) VALUES (1140, 7, N'Coca Cola', 13200, 330, CAST(28.75 AS Decimal(10, 2)), 10, CAST(330.00 AS Decimal(10, 2)), CAST(25.00 AS Decimal(18, 2)), 13200, 1)
INSERT [dbo].[Insumos] ([ID_Insumo], [ID_Unidad], [Nombre_insumo], [stock_total], [stock_minimo], [precio_lempiras], [ID_Categoria], [peso_individual], [precio_base], [stock_maximo], [ID_sucursal]) VALUES (1141, 1, N'Carne Grandota', 100, 5, CAST(115.00 AS Decimal(10, 2)), 2, CAST(1.00 AS Decimal(10, 2)), CAST(100.00 AS Decimal(18, 2)), 200, 1)
SET IDENTITY_INSERT [dbo].[Insumos] OFF
GO
SET IDENTITY_INSERT [dbo].[Jefe_de_cocina] ON 

INSERT [dbo].[Jefe_de_cocina] ([ID_Jefe_de_cocina], [Nombre], [apellido], [descripcion], [activo], [Username], [Password], [ID_sucursal]) VALUES (1, N'Luis', N'chuy', N'jefe de cocina', 1, N'luischuy', N'luis123', 1)
INSERT [dbo].[Jefe_de_cocina] ([ID_Jefe_de_cocina], [Nombre], [apellido], [descripcion], [activo], [Username], [Password], [ID_sucursal]) VALUES (2, N'Kevin Alejandro', N'Dsadws', N'Jefe de cocina', 1, N'kevin_jef', N'K3v!n190305', 1)
SET IDENTITY_INSERT [dbo].[Jefe_de_cocina] OFF
GO
SET IDENTITY_INSERT [dbo].[Metodos_money] ON 

INSERT [dbo].[Metodos_money] ([ID_Metodo], [Nombre], [Tipo], [Descripcion]) VALUES (1, N'Efectivo', 1, N'Pago en efectivo')
INSERT [dbo].[Metodos_money] ([ID_Metodo], [Nombre], [Tipo], [Descripcion]) VALUES (2, N'Tarjeta', 2, N'Pago con tarjeta de crédito o débito (solo últimos 4 dígitos)')
INSERT [dbo].[Metodos_money] ([ID_Metodo], [Nombre], [Tipo], [Descripcion]) VALUES (3, N'Mixto', 3, N'Pago combinado: efectivo + tarjeta')
SET IDENTITY_INSERT [dbo].[Metodos_money] OFF
GO
SET IDENTITY_INSERT [dbo].[Orden_Entrega] ON 

INSERT [dbo].[Orden_Entrega] ([ID_Orden_Entrega], [ID_Parametro], [Numero_Factura], [ID_Usuario_ClienteF], [nombre], [apellido], [ID_US_CO], [ID_Direccion], [descripcion], [telefono], [ID_sucursal], [ID_Empleado_Repartidor], [estado], [Fecha_Creacion], [Motivo_Cancelacion]) VALUES (2018, 2088, N'011-001-01-000216', 1, N'Kevin Alejandro', N'Herrera Guillen', 1, 1010, N'residencial plazas', N'99827720', 11, 19, 3, CAST(N'2025-12-14T06:59:24.010' AS DateTime), NULL)
INSERT [dbo].[Orden_Entrega] ([ID_Orden_Entrega], [ID_Parametro], [Numero_Factura], [ID_Usuario_ClienteF], [nombre], [apellido], [ID_US_CO], [ID_Direccion], [descripcion], [telefono], [ID_sucursal], [ID_Empleado_Repartidor], [estado], [Fecha_Creacion], [Motivo_Cancelacion]) VALUES (2019, 2089, N'011-001-01-000217', 1, N'Kevin Alejandro', N'Herrera Guillen', 1022, 1011, N'hola adios ejemplo', N'99827720', 11, 19, 0, CAST(N'2025-12-14T19:03:33.690' AS DateTime), NULL)
INSERT [dbo].[Orden_Entrega] ([ID_Orden_Entrega], [ID_Parametro], [Numero_Factura], [ID_Usuario_ClienteF], [nombre], [apellido], [ID_US_CO], [ID_Direccion], [descripcion], [telefono], [ID_sucursal], [ID_Empleado_Repartidor], [estado], [Fecha_Creacion], [Motivo_Cancelacion]) VALUES (2020, 2090, N'011-001-01-000218', 1, N'Kevin Alejandro', N'Herrera Guillen', 1, 1010, N'residencial plazas', N'99827720', 11, 19, 0, CAST(N'2025-12-14T20:31:00.353' AS DateTime), NULL)
INSERT [dbo].[Orden_Entrega] ([ID_Orden_Entrega], [ID_Parametro], [Numero_Factura], [ID_Usuario_ClienteF], [nombre], [apellido], [ID_US_CO], [ID_Direccion], [descripcion], [telefono], [ID_sucursal], [ID_Empleado_Repartidor], [estado], [Fecha_Creacion], [Motivo_Cancelacion]) VALUES (2021, 2091, N'011-001-01-000219', 1, N'Kevin Alejandro', N'Herrera Guillen', 1022, 1011, N'hola adios ejemplo', N'99827720', 11, 19, 2, CAST(N'2025-12-14T20:40:55.240' AS DateTime), NULL)
INSERT [dbo].[Orden_Entrega] ([ID_Orden_Entrega], [ID_Parametro], [Numero_Factura], [ID_Usuario_ClienteF], [nombre], [apellido], [ID_US_CO], [ID_Direccion], [descripcion], [telefono], [ID_sucursal], [ID_Empleado_Repartidor], [estado], [Fecha_Creacion], [Motivo_Cancelacion]) VALUES (2022, 2092, N'011-001-01-000220', 1, N'Kevin Alejandro', N'Herrera Guillen', 1022, 1011, N'hola adios ejemplo', N'99827720', 11, 19, 2, CAST(N'2025-12-14T21:44:29.953' AS DateTime), NULL)
INSERT [dbo].[Orden_Entrega] ([ID_Orden_Entrega], [ID_Parametro], [Numero_Factura], [ID_Usuario_ClienteF], [nombre], [apellido], [ID_US_CO], [ID_Direccion], [descripcion], [telefono], [ID_sucursal], [ID_Empleado_Repartidor], [estado], [Fecha_Creacion], [Motivo_Cancelacion]) VALUES (2023, 2093, N'011-001-01-000221', 1, N'Kevin Alejandro', N'Herrera Guillen', 1022, 1011, N'hola adios ejemplo', N'99827720', 11, 19, 3, CAST(N'2025-12-14T21:44:48.660' AS DateTime), NULL)
INSERT [dbo].[Orden_Entrega] ([ID_Orden_Entrega], [ID_Parametro], [Numero_Factura], [ID_Usuario_ClienteF], [nombre], [apellido], [ID_US_CO], [ID_Direccion], [descripcion], [telefono], [ID_sucursal], [ID_Empleado_Repartidor], [estado], [Fecha_Creacion], [Motivo_Cancelacion]) VALUES (2024, 2094, N'011-001-01-000222', 1, N'Kevin Alejandro', N'Herrera Guillen', 1, 1010, N'residencial plazas', N'99827720', 11, 19, 0, CAST(N'2026-02-01T21:36:54.137' AS DateTime), NULL)
SET IDENTITY_INSERT [dbo].[Orden_Entrega] OFF
GO
SET IDENTITY_INSERT [dbo].[Ordenes_Proveedores] ON 

INSERT [dbo].[Ordenes_Proveedores] ([ID_Orden_Proveedor], [ID_Proveedor], [ID_Empleado_Encargado], [ID_Sucursal], [Fecha_Inicio], [Fecha_Estimada], [Fecha_Entregado], [Estado], [Comentarios], [ID_Unidad], [Inventario_Aplicado], [Numero_Factura]) VALUES (4, 1, 22, 11, CAST(N'2025-12-12T09:58:29.0000000' AS DateTime2), CAST(N'2025-12-31T00:00:00.0000000' AS DateTime2), CAST(N'2025-12-12T00:00:00.0000000' AS DateTime2), 2, NULL, NULL, 0, NULL)
INSERT [dbo].[Ordenes_Proveedores] ([ID_Orden_Proveedor], [ID_Proveedor], [ID_Empleado_Encargado], [ID_Sucursal], [Fecha_Inicio], [Fecha_Estimada], [Fecha_Entregado], [Estado], [Comentarios], [ID_Unidad], [Inventario_Aplicado], [Numero_Factura]) VALUES (5, 1, 22, 11, CAST(N'2025-12-12T10:39:25.0000000' AS DateTime2), CAST(N'2025-12-22T00:00:00.0000000' AS DateTime2), CAST(N'2025-12-14T08:12:08.0000000' AS DateTime2), 2, N'si', NULL, 0, N'01101010101010')
INSERT [dbo].[Ordenes_Proveedores] ([ID_Orden_Proveedor], [ID_Proveedor], [ID_Empleado_Encargado], [ID_Sucursal], [Fecha_Inicio], [Fecha_Estimada], [Fecha_Entregado], [Estado], [Comentarios], [ID_Unidad], [Inventario_Aplicado], [Numero_Factura]) VALUES (6, 1, 22, 11, CAST(N'2025-12-12T10:54:01.0000000' AS DateTime2), CAST(N'2025-12-16T00:00:00.0000000' AS DateTime2), CAST(N'2025-12-14T08:24:44.0000000' AS DateTime2), 2, NULL, NULL, 0, N'12321321332123')
INSERT [dbo].[Ordenes_Proveedores] ([ID_Orden_Proveedor], [ID_Proveedor], [ID_Empleado_Encargado], [ID_Sucursal], [Fecha_Inicio], [Fecha_Estimada], [Fecha_Entregado], [Estado], [Comentarios], [ID_Unidad], [Inventario_Aplicado], [Numero_Factura]) VALUES (7, 1, 22, 11, CAST(N'2025-12-12T11:07:08.0000000' AS DateTime2), CAST(N'2025-12-31T00:00:00.0000000' AS DateTime2), CAST(N'2025-12-14T17:55:47.0000000' AS DateTime2), 2, NULL, NULL, 0, N'32123312321239')
INSERT [dbo].[Ordenes_Proveedores] ([ID_Orden_Proveedor], [ID_Proveedor], [ID_Empleado_Encargado], [ID_Sucursal], [Fecha_Inicio], [Fecha_Estimada], [Fecha_Entregado], [Estado], [Comentarios], [ID_Unidad], [Inventario_Aplicado], [Numero_Factura]) VALUES (8, 1, 22, 11, CAST(N'2025-12-12T12:02:14.0000000' AS DateTime2), CAST(N'2025-12-31T00:00:00.0000000' AS DateTime2), CAST(N'2026-01-01T00:00:00.0000000' AS DateTime2), 2, NULL, NULL, 0, N'11111111111111')
INSERT [dbo].[Ordenes_Proveedores] ([ID_Orden_Proveedor], [ID_Proveedor], [ID_Empleado_Encargado], [ID_Sucursal], [Fecha_Inicio], [Fecha_Estimada], [Fecha_Entregado], [Estado], [Comentarios], [ID_Unidad], [Inventario_Aplicado], [Numero_Factura]) VALUES (9, 1, 22, 11, CAST(N'2025-12-12T12:02:16.0000000' AS DateTime2), CAST(N'2025-12-14T00:00:00.0000000' AS DateTime2), CAST(N'2026-01-01T00:00:00.0000000' AS DateTime2), 2, NULL, NULL, 0, N'11111111111111')
INSERT [dbo].[Ordenes_Proveedores] ([ID_Orden_Proveedor], [ID_Proveedor], [ID_Empleado_Encargado], [ID_Sucursal], [Fecha_Inicio], [Fecha_Estimada], [Fecha_Entregado], [Estado], [Comentarios], [ID_Unidad], [Inventario_Aplicado], [Numero_Factura]) VALUES (10, 1, 22, 11, CAST(N'2025-12-12T12:02:17.0000000' AS DateTime2), CAST(N'2025-12-14T00:00:00.0000000' AS DateTime2), CAST(N'2025-12-14T00:00:00.0000000' AS DateTime2), 2, NULL, NULL, 0, N'32132131231222')
INSERT [dbo].[Ordenes_Proveedores] ([ID_Orden_Proveedor], [ID_Proveedor], [ID_Empleado_Encargado], [ID_Sucursal], [Fecha_Inicio], [Fecha_Estimada], [Fecha_Entregado], [Estado], [Comentarios], [ID_Unidad], [Inventario_Aplicado], [Numero_Factura]) VALUES (11, 1, 22, 11, CAST(N'2025-12-12T12:02:17.0000000' AS DateTime2), CAST(N'2025-12-14T00:00:00.0000000' AS DateTime2), CAST(N'2025-12-14T00:00:00.0000000' AS DateTime2), 2, NULL, NULL, 0, N'11111111111111')
INSERT [dbo].[Ordenes_Proveedores] ([ID_Orden_Proveedor], [ID_Proveedor], [ID_Empleado_Encargado], [ID_Sucursal], [Fecha_Inicio], [Fecha_Estimada], [Fecha_Entregado], [Estado], [Comentarios], [ID_Unidad], [Inventario_Aplicado], [Numero_Factura]) VALUES (12, 1, 22, 11, CAST(N'2025-12-12T12:02:17.0000000' AS DateTime2), CAST(N'2025-12-27T00:00:00.0000000' AS DateTime2), CAST(N'2025-12-14T00:00:00.0000000' AS DateTime2), 2, NULL, NULL, 0, N'11111111111111')
INSERT [dbo].[Ordenes_Proveedores] ([ID_Orden_Proveedor], [ID_Proveedor], [ID_Empleado_Encargado], [ID_Sucursal], [Fecha_Inicio], [Fecha_Estimada], [Fecha_Entregado], [Estado], [Comentarios], [ID_Unidad], [Inventario_Aplicado], [Numero_Factura]) VALUES (13, 1, 22, 11, CAST(N'2025-12-12T14:14:22.0000000' AS DateTime2), NULL, CAST(N'2025-12-12T00:00:00.0000000' AS DateTime2), 2, NULL, NULL, 0, NULL)
INSERT [dbo].[Ordenes_Proveedores] ([ID_Orden_Proveedor], [ID_Proveedor], [ID_Empleado_Encargado], [ID_Sucursal], [Fecha_Inicio], [Fecha_Estimada], [Fecha_Entregado], [Estado], [Comentarios], [ID_Unidad], [Inventario_Aplicado], [Numero_Factura]) VALUES (14, 5, 22, 11, CAST(N'2025-12-14T06:17:00.0000000' AS DateTime2), CAST(N'2025-12-23T00:00:00.0000000' AS DateTime2), CAST(N'2025-12-24T00:00:00.0000000' AS DateTime2), 2, NULL, NULL, 0, N'00011010101012')
INSERT [dbo].[Ordenes_Proveedores] ([ID_Orden_Proveedor], [ID_Proveedor], [ID_Empleado_Encargado], [ID_Sucursal], [Fecha_Inicio], [Fecha_Estimada], [Fecha_Entregado], [Estado], [Comentarios], [ID_Unidad], [Inventario_Aplicado], [Numero_Factura]) VALUES (15, 1, 22, 11, CAST(N'2025-12-14T06:17:02.0000000' AS DateTime2), CAST(N'2025-12-31T00:00:00.0000000' AS DateTime2), CAST(N'2025-12-14T06:24:35.0000000' AS DateTime2), 2, NULL, NULL, 0, N'01001101010101')
INSERT [dbo].[Ordenes_Proveedores] ([ID_Orden_Proveedor], [ID_Proveedor], [ID_Empleado_Encargado], [ID_Sucursal], [Fecha_Inicio], [Fecha_Estimada], [Fecha_Entregado], [Estado], [Comentarios], [ID_Unidad], [Inventario_Aplicado], [Numero_Factura]) VALUES (16, 5, 22, 11, CAST(N'2025-12-14T17:41:31.0000000' AS DateTime2), CAST(N'2025-12-14T00:00:00.0000000' AS DateTime2), CAST(N'2025-12-14T00:00:00.0000000' AS DateTime2), 2, NULL, NULL, 0, N'10101010101010')
INSERT [dbo].[Ordenes_Proveedores] ([ID_Orden_Proveedor], [ID_Proveedor], [ID_Empleado_Encargado], [ID_Sucursal], [Fecha_Inicio], [Fecha_Estimada], [Fecha_Entregado], [Estado], [Comentarios], [ID_Unidad], [Inventario_Aplicado], [Numero_Factura]) VALUES (17, 5, 22, 1, CAST(N'2025-12-14T17:41:31.0000000' AS DateTime2), CAST(N'2025-12-31T00:00:00.0000000' AS DateTime2), CAST(N'2025-12-30T00:00:00.0000000' AS DateTime2), 2, NULL, NULL, 0, N'11111111111111')
INSERT [dbo].[Ordenes_Proveedores] ([ID_Orden_Proveedor], [ID_Proveedor], [ID_Empleado_Encargado], [ID_Sucursal], [Fecha_Inicio], [Fecha_Estimada], [Fecha_Entregado], [Estado], [Comentarios], [ID_Unidad], [Inventario_Aplicado], [Numero_Factura]) VALUES (18, 5, 22, 11, CAST(N'2025-12-14T23:57:16.0000000' AS DateTime2), NULL, NULL, 3, NULL, NULL, 0, NULL)
INSERT [dbo].[Ordenes_Proveedores] ([ID_Orden_Proveedor], [ID_Proveedor], [ID_Empleado_Encargado], [ID_Sucursal], [Fecha_Inicio], [Fecha_Estimada], [Fecha_Entregado], [Estado], [Comentarios], [ID_Unidad], [Inventario_Aplicado], [Numero_Factura]) VALUES (19, 5, 22, 1, CAST(N'2025-12-14T23:57:16.0000000' AS DateTime2), NULL, NULL, 3, NULL, NULL, 0, NULL)
INSERT [dbo].[Ordenes_Proveedores] ([ID_Orden_Proveedor], [ID_Proveedor], [ID_Empleado_Encargado], [ID_Sucursal], [Fecha_Inicio], [Fecha_Estimada], [Fecha_Entregado], [Estado], [Comentarios], [ID_Unidad], [Inventario_Aplicado], [Numero_Factura]) VALUES (20, 5, 22, 11, CAST(N'2025-12-15T00:25:11.0000000' AS DateTime2), NULL, NULL, 3, NULL, NULL, 0, NULL)
INSERT [dbo].[Ordenes_Proveedores] ([ID_Orden_Proveedor], [ID_Proveedor], [ID_Empleado_Encargado], [ID_Sucursal], [Fecha_Inicio], [Fecha_Estimada], [Fecha_Entregado], [Estado], [Comentarios], [ID_Unidad], [Inventario_Aplicado], [Numero_Factura]) VALUES (21, 5, 22, 1, CAST(N'2025-12-15T00:25:11.0000000' AS DateTime2), CAST(N'2025-12-30T00:00:00.0000000' AS DateTime2), CAST(N'2026-01-01T00:00:00.0000000' AS DateTime2), 2, NULL, NULL, 0, N'31232112312312')
INSERT [dbo].[Ordenes_Proveedores] ([ID_Orden_Proveedor], [ID_Proveedor], [ID_Empleado_Encargado], [ID_Sucursal], [Fecha_Inicio], [Fecha_Estimada], [Fecha_Entregado], [Estado], [Comentarios], [ID_Unidad], [Inventario_Aplicado], [Numero_Factura]) VALUES (22, 5, 22, 11, CAST(N'2025-12-15T02:36:58.0000000' AS DateTime2), CAST(N'2025-12-20T00:00:00.0000000' AS DateTime2), CAST(N'2025-12-21T00:00:00.0000000' AS DateTime2), 2, NULL, NULL, 0, N'01010110232245')
INSERT [dbo].[Ordenes_Proveedores] ([ID_Orden_Proveedor], [ID_Proveedor], [ID_Empleado_Encargado], [ID_Sucursal], [Fecha_Inicio], [Fecha_Estimada], [Fecha_Entregado], [Estado], [Comentarios], [ID_Unidad], [Inventario_Aplicado], [Numero_Factura]) VALUES (23, 5, 22, 1, CAST(N'2025-12-15T02:36:58.0000000' AS DateTime2), NULL, NULL, 0, NULL, NULL, 0, NULL)
INSERT [dbo].[Ordenes_Proveedores] ([ID_Orden_Proveedor], [ID_Proveedor], [ID_Empleado_Encargado], [ID_Sucursal], [Fecha_Inicio], [Fecha_Estimada], [Fecha_Entregado], [Estado], [Comentarios], [ID_Unidad], [Inventario_Aplicado], [Numero_Factura]) VALUES (24, 1, 22, 11, CAST(N'2025-12-15T03:48:41.0000000' AS DateTime2), NULL, NULL, 0, NULL, NULL, 0, NULL)
INSERT [dbo].[Ordenes_Proveedores] ([ID_Orden_Proveedor], [ID_Proveedor], [ID_Empleado_Encargado], [ID_Sucursal], [Fecha_Inicio], [Fecha_Estimada], [Fecha_Entregado], [Estado], [Comentarios], [ID_Unidad], [Inventario_Aplicado], [Numero_Factura]) VALUES (25, 5, 22, 1, CAST(N'2026-01-13T01:41:14.0000000' AS DateTime2), CAST(N'2026-01-20T00:00:00.0000000' AS DateTime2), CAST(N'2026-01-21T00:00:00.0000000' AS DateTime2), 2, N'si', NULL, 0, N'00101010101101')
SET IDENTITY_INSERT [dbo].[Ordenes_Proveedores] OFF
GO
SET IDENTITY_INSERT [dbo].[Ordenes_Proveedores_Detalle] ON 

INSERT [dbo].[Ordenes_Proveedores_Detalle] ([ID_Detalle], [ID_Orden_Proveedor], [ID_Insumo], [ID_Unidad], [Cantidad_Solicitada], [Cantidad_Recibida], [ID_Unidad_Recibida]) VALUES (1, 4, 6, 3, 21, 20, 3)
INSERT [dbo].[Ordenes_Proveedores_Detalle] ([ID_Detalle], [ID_Orden_Proveedor], [ID_Insumo], [ID_Unidad], [Cantidad_Solicitada], [Cantidad_Recibida], [ID_Unidad_Recibida]) VALUES (2, 5, 5, 3, 10, 5, 3)
INSERT [dbo].[Ordenes_Proveedores_Detalle] ([ID_Detalle], [ID_Orden_Proveedor], [ID_Insumo], [ID_Unidad], [Cantidad_Solicitada], [Cantidad_Recibida], [ID_Unidad_Recibida]) VALUES (3, 6, 5, 3, 10, 1, 3)
INSERT [dbo].[Ordenes_Proveedores_Detalle] ([ID_Detalle], [ID_Orden_Proveedor], [ID_Insumo], [ID_Unidad], [Cantidad_Solicitada], [Cantidad_Recibida], [ID_Unidad_Recibida]) VALUES (4, 7, 5, 3, 20, 15, 3)
INSERT [dbo].[Ordenes_Proveedores_Detalle] ([ID_Detalle], [ID_Orden_Proveedor], [ID_Insumo], [ID_Unidad], [Cantidad_Solicitada], [Cantidad_Recibida], [ID_Unidad_Recibida]) VALUES (5, 8, 5, 3, 20, 20, 3)
INSERT [dbo].[Ordenes_Proveedores_Detalle] ([ID_Detalle], [ID_Orden_Proveedor], [ID_Insumo], [ID_Unidad], [Cantidad_Solicitada], [Cantidad_Recibida], [ID_Unidad_Recibida]) VALUES (6, 9, 5, 3, 20, 3, 3)
INSERT [dbo].[Ordenes_Proveedores_Detalle] ([ID_Detalle], [ID_Orden_Proveedor], [ID_Insumo], [ID_Unidad], [Cantidad_Solicitada], [Cantidad_Recibida], [ID_Unidad_Recibida]) VALUES (7, 11, 5, 3, 20, 12, 3)
INSERT [dbo].[Ordenes_Proveedores_Detalle] ([ID_Detalle], [ID_Orden_Proveedor], [ID_Insumo], [ID_Unidad], [Cantidad_Solicitada], [Cantidad_Recibida], [ID_Unidad_Recibida]) VALUES (8, 12, 5, 3, 20, 19.2, 3)
INSERT [dbo].[Ordenes_Proveedores_Detalle] ([ID_Detalle], [ID_Orden_Proveedor], [ID_Insumo], [ID_Unidad], [Cantidad_Solicitada], [Cantidad_Recibida], [ID_Unidad_Recibida]) VALUES (9, 10, 5, 3, 20, 12, 3)
INSERT [dbo].[Ordenes_Proveedores_Detalle] ([ID_Detalle], [ID_Orden_Proveedor], [ID_Insumo], [ID_Unidad], [Cantidad_Solicitada], [Cantidad_Recibida], [ID_Unidad_Recibida]) VALUES (10, 13, 5, 3, 15, 20, 3)
INSERT [dbo].[Ordenes_Proveedores_Detalle] ([ID_Detalle], [ID_Orden_Proveedor], [ID_Insumo], [ID_Unidad], [Cantidad_Solicitada], [Cantidad_Recibida], [ID_Unidad_Recibida]) VALUES (11, 14, 5, 3, 100, 90, 3)
INSERT [dbo].[Ordenes_Proveedores_Detalle] ([ID_Detalle], [ID_Orden_Proveedor], [ID_Insumo], [ID_Unidad], [Cantidad_Solicitada], [Cantidad_Recibida], [ID_Unidad_Recibida]) VALUES (12, 15, 5, 3, 100, 20, 3)
INSERT [dbo].[Ordenes_Proveedores_Detalle] ([ID_Detalle], [ID_Orden_Proveedor], [ID_Insumo], [ID_Unidad], [Cantidad_Solicitada], [Cantidad_Recibida], [ID_Unidad_Recibida]) VALUES (13, 16, 81, 1, 10, 2, 1)
INSERT [dbo].[Ordenes_Proveedores_Detalle] ([ID_Detalle], [ID_Orden_Proveedor], [ID_Insumo], [ID_Unidad], [Cantidad_Solicitada], [Cantidad_Recibida], [ID_Unidad_Recibida]) VALUES (14, 16, 5, 3, 10, 2, 3)
INSERT [dbo].[Ordenes_Proveedores_Detalle] ([ID_Detalle], [ID_Orden_Proveedor], [ID_Insumo], [ID_Unidad], [Cantidad_Solicitada], [Cantidad_Recibida], [ID_Unidad_Recibida]) VALUES (15, 17, 138, 3, 10, 5, 3)
INSERT [dbo].[Ordenes_Proveedores_Detalle] ([ID_Detalle], [ID_Orden_Proveedor], [ID_Insumo], [ID_Unidad], [Cantidad_Solicitada], [Cantidad_Recibida], [ID_Unidad_Recibida]) VALUES (16, 18, 9, 3, 10, 0, NULL)
INSERT [dbo].[Ordenes_Proveedores_Detalle] ([ID_Detalle], [ID_Orden_Proveedor], [ID_Insumo], [ID_Unidad], [Cantidad_Solicitada], [Cantidad_Recibida], [ID_Unidad_Recibida]) VALUES (17, 18, 7, 3, 10, 0, NULL)
INSERT [dbo].[Ordenes_Proveedores_Detalle] ([ID_Detalle], [ID_Orden_Proveedor], [ID_Insumo], [ID_Unidad], [Cantidad_Solicitada], [Cantidad_Recibida], [ID_Unidad_Recibida]) VALUES (18, 19, 1139, 6, 10, 0, NULL)
INSERT [dbo].[Ordenes_Proveedores_Detalle] ([ID_Detalle], [ID_Orden_Proveedor], [ID_Insumo], [ID_Unidad], [Cantidad_Solicitada], [Cantidad_Recibida], [ID_Unidad_Recibida]) VALUES (19, 19, 1138, 3, 10, 0, NULL)
INSERT [dbo].[Ordenes_Proveedores_Detalle] ([ID_Detalle], [ID_Orden_Proveedor], [ID_Insumo], [ID_Unidad], [Cantidad_Solicitada], [Cantidad_Recibida], [ID_Unidad_Recibida]) VALUES (20, 19, 138, 3, 10, 0, NULL)
INSERT [dbo].[Ordenes_Proveedores_Detalle] ([ID_Detalle], [ID_Orden_Proveedor], [ID_Insumo], [ID_Unidad], [Cantidad_Solicitada], [Cantidad_Recibida], [ID_Unidad_Recibida]) VALUES (21, 20, 15, 6, 12, 0, NULL)
INSERT [dbo].[Ordenes_Proveedores_Detalle] ([ID_Detalle], [ID_Orden_Proveedor], [ID_Insumo], [ID_Unidad], [Cantidad_Solicitada], [Cantidad_Recibida], [ID_Unidad_Recibida]) VALUES (22, 20, 11, 3, 10, 0, NULL)
INSERT [dbo].[Ordenes_Proveedores_Detalle] ([ID_Detalle], [ID_Orden_Proveedor], [ID_Insumo], [ID_Unidad], [Cantidad_Solicitada], [Cantidad_Recibida], [ID_Unidad_Recibida]) VALUES (23, 21, 1139, 6, 10, 10, 6)
INSERT [dbo].[Ordenes_Proveedores_Detalle] ([ID_Detalle], [ID_Orden_Proveedor], [ID_Insumo], [ID_Unidad], [Cantidad_Solicitada], [Cantidad_Recibida], [ID_Unidad_Recibida]) VALUES (24, 21, 1138, 3, 20, 15, 3)
INSERT [dbo].[Ordenes_Proveedores_Detalle] ([ID_Detalle], [ID_Orden_Proveedor], [ID_Insumo], [ID_Unidad], [Cantidad_Solicitada], [Cantidad_Recibida], [ID_Unidad_Recibida]) VALUES (25, 22, 81, 1, 10, 8, 1)
INSERT [dbo].[Ordenes_Proveedores_Detalle] ([ID_Detalle], [ID_Orden_Proveedor], [ID_Insumo], [ID_Unidad], [Cantidad_Solicitada], [Cantidad_Recibida], [ID_Unidad_Recibida]) VALUES (26, 22, 23, 6, 10, 8, 6)
INSERT [dbo].[Ordenes_Proveedores_Detalle] ([ID_Detalle], [ID_Orden_Proveedor], [ID_Insumo], [ID_Unidad], [Cantidad_Solicitada], [Cantidad_Recibida], [ID_Unidad_Recibida]) VALUES (27, 23, 1139, 6, 200, 0, NULL)
INSERT [dbo].[Ordenes_Proveedores_Detalle] ([ID_Detalle], [ID_Orden_Proveedor], [ID_Insumo], [ID_Unidad], [Cantidad_Solicitada], [Cantidad_Recibida], [ID_Unidad_Recibida]) VALUES (28, 23, 1138, 3, 100, 0, NULL)
INSERT [dbo].[Ordenes_Proveedores_Detalle] ([ID_Detalle], [ID_Orden_Proveedor], [ID_Insumo], [ID_Unidad], [Cantidad_Solicitada], [Cantidad_Recibida], [ID_Unidad_Recibida]) VALUES (29, 24, 7, 3, 122, 0, NULL)
INSERT [dbo].[Ordenes_Proveedores_Detalle] ([ID_Detalle], [ID_Orden_Proveedor], [ID_Insumo], [ID_Unidad], [Cantidad_Solicitada], [Cantidad_Recibida], [ID_Unidad_Recibida]) VALUES (30, 25, 1138, 3, 50, 48, 3)
SET IDENTITY_INSERT [dbo].[Ordenes_Proveedores_Detalle] OFF
GO
SET IDENTITY_INSERT [dbo].[pago_detalle] ON 

INSERT [dbo].[pago_detalle] ([ID_pago], [ID_Metodo], [Efectivo], [Numero_tarjeta]) VALUES (1, 1, CAST(51.06 AS Decimal(18, 2)), NULL)
INSERT [dbo].[pago_detalle] ([ID_pago], [ID_Metodo], [Efectivo], [Numero_tarjeta]) VALUES (2, 1, CAST(51.06 AS Decimal(18, 2)), NULL)
INSERT [dbo].[pago_detalle] ([ID_pago], [ID_Metodo], [Efectivo], [Numero_tarjeta]) VALUES (3, 1, CAST(51.06 AS Decimal(18, 2)), NULL)
INSERT [dbo].[pago_detalle] ([ID_pago], [ID_Metodo], [Efectivo], [Numero_tarjeta]) VALUES (4, 2, NULL, N'3312')
INSERT [dbo].[pago_detalle] ([ID_pago], [ID_Metodo], [Efectivo], [Numero_tarjeta]) VALUES (5, 2, NULL, N'3312')
INSERT [dbo].[pago_detalle] ([ID_pago], [ID_Metodo], [Efectivo], [Numero_tarjeta]) VALUES (6, 2, NULL, N'3312')
INSERT [dbo].[pago_detalle] ([ID_pago], [ID_Metodo], [Efectivo], [Numero_tarjeta]) VALUES (7, 1, CAST(29.40 AS Decimal(18, 2)), NULL)
SET IDENTITY_INSERT [dbo].[pago_detalle] OFF
GO
SET IDENTITY_INSERT [dbo].[Pagos_cliente] ON 

INSERT [dbo].[Pagos_cliente] ([ID_Pago], [ID_Usuario_ClienteF], [ID_Metodo], [Cantidad], [Numero_tarjeta], [a_nombre_de]) VALUES (2, 1, 2, NULL, N'3312', N'kevin')
SET IDENTITY_INSERT [dbo].[Pagos_cliente] OFF
GO
SET IDENTITY_INSERT [dbo].[Parametros_SAR] ON 

INSERT [dbo].[Parametros_SAR] ([ID_Parametro], [Parametro], [Valor]) VALUES (1, N'factura', N'01')
INSERT [dbo].[Parametros_SAR] ([ID_Parametro], [Parametro], [Valor]) VALUES (2, N'notas de débito', N'02')
INSERT [dbo].[Parametros_SAR] ([ID_Parametro], [Parametro], [Valor]) VALUES (3, N'Devolución', N'03')
INSERT [dbo].[Parametros_SAR] ([ID_Parametro], [Parametro], [Valor]) VALUES (4, N'rtn', N'08012005095147')
INSERT [dbo].[Parametros_SAR] ([ID_Parametro], [Parametro], [Valor]) VALUES (5, N'caja', N'001')
SET IDENTITY_INSERT [dbo].[Parametros_SAR] OFF
GO
SET IDENTITY_INSERT [dbo].[Proveedor_Insumo] ON 

INSERT [dbo].[Proveedor_Insumo] ([ID_Proveedor_Insumo], [ID_Proveedor], [ID_Insumo], [Activo]) VALUES (1, 1, 5, 1)
INSERT [dbo].[Proveedor_Insumo] ([ID_Proveedor_Insumo], [ID_Proveedor], [ID_Insumo], [Activo]) VALUES (2, 1, 6, 1)
INSERT [dbo].[Proveedor_Insumo] ([ID_Proveedor_Insumo], [ID_Proveedor], [ID_Insumo], [Activo]) VALUES (3, 1, 7, 1)
INSERT [dbo].[Proveedor_Insumo] ([ID_Proveedor_Insumo], [ID_Proveedor], [ID_Insumo], [Activo]) VALUES (4, 5, 4, 1)
INSERT [dbo].[Proveedor_Insumo] ([ID_Proveedor_Insumo], [ID_Proveedor], [ID_Insumo], [Activo]) VALUES (5, 5, 5, 1)
INSERT [dbo].[Proveedor_Insumo] ([ID_Proveedor_Insumo], [ID_Proveedor], [ID_Insumo], [Activo]) VALUES (6, 5, 7, 1)
INSERT [dbo].[Proveedor_Insumo] ([ID_Proveedor_Insumo], [ID_Proveedor], [ID_Insumo], [Activo]) VALUES (7, 5, 9, 1)
INSERT [dbo].[Proveedor_Insumo] ([ID_Proveedor_Insumo], [ID_Proveedor], [ID_Insumo], [Activo]) VALUES (8, 5, 11, 1)
INSERT [dbo].[Proveedor_Insumo] ([ID_Proveedor_Insumo], [ID_Proveedor], [ID_Insumo], [Activo]) VALUES (9, 5, 15, 1)
INSERT [dbo].[Proveedor_Insumo] ([ID_Proveedor_Insumo], [ID_Proveedor], [ID_Insumo], [Activo]) VALUES (10, 5, 17, 1)
INSERT [dbo].[Proveedor_Insumo] ([ID_Proveedor_Insumo], [ID_Proveedor], [ID_Insumo], [Activo]) VALUES (11, 5, 20, 1)
INSERT [dbo].[Proveedor_Insumo] ([ID_Proveedor_Insumo], [ID_Proveedor], [ID_Insumo], [Activo]) VALUES (12, 5, 23, 1)
INSERT [dbo].[Proveedor_Insumo] ([ID_Proveedor_Insumo], [ID_Proveedor], [ID_Insumo], [Activo]) VALUES (13, 5, 24, 1)
INSERT [dbo].[Proveedor_Insumo] ([ID_Proveedor_Insumo], [ID_Proveedor], [ID_Insumo], [Activo]) VALUES (14, 5, 27, 1)
INSERT [dbo].[Proveedor_Insumo] ([ID_Proveedor_Insumo], [ID_Proveedor], [ID_Insumo], [Activo]) VALUES (15, 5, 29, 1)
INSERT [dbo].[Proveedor_Insumo] ([ID_Proveedor_Insumo], [ID_Proveedor], [ID_Insumo], [Activo]) VALUES (16, 5, 31, 1)
INSERT [dbo].[Proveedor_Insumo] ([ID_Proveedor_Insumo], [ID_Proveedor], [ID_Insumo], [Activo]) VALUES (17, 5, 35, 1)
INSERT [dbo].[Proveedor_Insumo] ([ID_Proveedor_Insumo], [ID_Proveedor], [ID_Insumo], [Activo]) VALUES (18, 5, 37, 1)
INSERT [dbo].[Proveedor_Insumo] ([ID_Proveedor_Insumo], [ID_Proveedor], [ID_Insumo], [Activo]) VALUES (19, 5, 40, 1)
INSERT [dbo].[Proveedor_Insumo] ([ID_Proveedor_Insumo], [ID_Proveedor], [ID_Insumo], [Activo]) VALUES (20, 5, 41, 1)
INSERT [dbo].[Proveedor_Insumo] ([ID_Proveedor_Insumo], [ID_Proveedor], [ID_Insumo], [Activo]) VALUES (21, 5, 45, 1)
INSERT [dbo].[Proveedor_Insumo] ([ID_Proveedor_Insumo], [ID_Proveedor], [ID_Insumo], [Activo]) VALUES (22, 5, 46, 1)
INSERT [dbo].[Proveedor_Insumo] ([ID_Proveedor_Insumo], [ID_Proveedor], [ID_Insumo], [Activo]) VALUES (23, 5, 49, 1)
INSERT [dbo].[Proveedor_Insumo] ([ID_Proveedor_Insumo], [ID_Proveedor], [ID_Insumo], [Activo]) VALUES (24, 5, 52, 1)
INSERT [dbo].[Proveedor_Insumo] ([ID_Proveedor_Insumo], [ID_Proveedor], [ID_Insumo], [Activo]) VALUES (25, 5, 54, 1)
INSERT [dbo].[Proveedor_Insumo] ([ID_Proveedor_Insumo], [ID_Proveedor], [ID_Insumo], [Activo]) VALUES (26, 5, 58, 1)
INSERT [dbo].[Proveedor_Insumo] ([ID_Proveedor_Insumo], [ID_Proveedor], [ID_Insumo], [Activo]) VALUES (27, 5, 60, 1)
INSERT [dbo].[Proveedor_Insumo] ([ID_Proveedor_Insumo], [ID_Proveedor], [ID_Insumo], [Activo]) VALUES (28, 5, 63, 1)
INSERT [dbo].[Proveedor_Insumo] ([ID_Proveedor_Insumo], [ID_Proveedor], [ID_Insumo], [Activo]) VALUES (29, 5, 81, 1)
INSERT [dbo].[Proveedor_Insumo] ([ID_Proveedor_Insumo], [ID_Proveedor], [ID_Insumo], [Activo]) VALUES (30, 5, 138, 1)
INSERT [dbo].[Proveedor_Insumo] ([ID_Proveedor_Insumo], [ID_Proveedor], [ID_Insumo], [Activo]) VALUES (31, 5, 1138, 1)
INSERT [dbo].[Proveedor_Insumo] ([ID_Proveedor_Insumo], [ID_Proveedor], [ID_Insumo], [Activo]) VALUES (32, 5, 1139, 1)
SET IDENTITY_INSERT [dbo].[Proveedor_Insumo] OFF
GO
SET IDENTITY_INSERT [dbo].[Proveedores] ON 

INSERT [dbo].[Proveedores] ([ID_Proveedor], [Telefono], [email], [activo], [Nombre_Proveedor]) VALUES (1, 98765432, N'kevinherg2015@gmail.com', 1, N'Proveedor Ejemplo')
INSERT [dbo].[Proveedores] ([ID_Proveedor], [Telefono], [email], [activo], [Nombre_Proveedor]) VALUES (5, 32121222, N'kevinherg2002@gmail.com', 1, N'Proveedor Ejemplo Dos')
SET IDENTITY_INSERT [dbo].[Proveedores] OFF
GO
SET IDENTITY_INSERT [dbo].[Puesto] ON 

INSERT [dbo].[Puesto] ([ID_Puesto], [Nombre_Puesto], [estado]) VALUES (1, N'Jefe de Cocina', 1)
INSERT [dbo].[Puesto] ([ID_Puesto], [Nombre_Puesto], [estado]) VALUES (2, N'Cocinero', 1)
INSERT [dbo].[Puesto] ([ID_Puesto], [Nombre_Puesto], [estado]) VALUES (3, N'Mesero', 1)
INSERT [dbo].[Puesto] ([ID_Puesto], [Nombre_Puesto], [estado]) VALUES (4, N'Repartidor', 1)
INSERT [dbo].[Puesto] ([ID_Puesto], [Nombre_Puesto], [estado]) VALUES (5, N'Caja', 1)
INSERT [dbo].[Puesto] ([ID_Puesto], [Nombre_Puesto], [estado]) VALUES (6, N'Administrador', 1)
INSERT [dbo].[Puesto] ([ID_Puesto], [Nombre_Puesto], [estado]) VALUES (9, N'Ejemplo', 0)
INSERT [dbo].[Puesto] ([ID_Puesto], [Nombre_Puesto], [estado]) VALUES (10, N'Contador', 1)
INSERT [dbo].[Puesto] ([ID_Puesto], [Nombre_Puesto], [estado]) VALUES (11, N'Cajero Web', 1)
INSERT [dbo].[Puesto] ([ID_Puesto], [Nombre_Puesto], [estado]) VALUES (12, N'Emitidor De Facturas', 1)
INSERT [dbo].[Puesto] ([ID_Puesto], [Nombre_Puesto], [estado]) VALUES (13, N'Cajero', 1)
INSERT [dbo].[Puesto] ([ID_Puesto], [Nombre_Puesto], [estado]) VALUES (14, N'Encargado De Compras Insumos', 1)
INSERT [dbo].[Puesto] ([ID_Puesto], [Nombre_Puesto], [estado]) VALUES (15, N'Cliente Final', 1)
INSERT [dbo].[Puesto] ([ID_Puesto], [Nombre_Puesto], [estado]) VALUES (16, N'Gerente', 1)
SET IDENTITY_INSERT [dbo].[Puesto] OFF
GO
SET IDENTITY_INSERT [dbo].[Recetas] ON 

INSERT [dbo].[Recetas] ([ID_Receta], [ID_Jefe_de_cocina], [Nombre_receta], [Estado], [descripcion], [categoria], [descripcion_cliente], [ID_sucursal]) VALUES (2104, 1, N'ejemplo', 1, N'qwerty', 1, N'dwq', 11)
INSERT [dbo].[Recetas] ([ID_Receta], [ID_Jefe_de_cocina], [Nombre_receta], [Estado], [descripcion], [categoria], [descripcion_cliente], [ID_sucursal]) VALUES (2105, 1, N'ejemplo1', 1, N'dsa', 2, N'dwq', 11)
INSERT [dbo].[Recetas] ([ID_Receta], [ID_Jefe_de_cocina], [Nombre_receta], [Estado], [descripcion], [categoria], [descripcion_cliente], [ID_sucursal]) VALUES (2106, 1, N'ejemploqq', 1, N'dsa', 1, N'hola', 11)
INSERT [dbo].[Recetas] ([ID_Receta], [ID_Jefe_de_cocina], [Nombre_receta], [Estado], [descripcion], [categoria], [descripcion_cliente], [ID_sucursal]) VALUES (2107, 1, N'ejemplo aa', 1, N'dsa', 3, N'dsa', 11)
INSERT [dbo].[Recetas] ([ID_Receta], [ID_Jefe_de_cocina], [Nombre_receta], [Estado], [descripcion], [categoria], [descripcion_cliente], [ID_sucursal]) VALUES (2108, 1, N'Alitas BBQ', 1, N'alitas', 1, N'alitas con bbq', 11)
INSERT [dbo].[Recetas] ([ID_Receta], [ID_Jefe_de_cocina], [Nombre_receta], [Estado], [descripcion], [categoria], [descripcion_cliente], [ID_sucursal]) VALUES (2109, 1, N'limonada', 1, N'limonada', 3, N'limonada', 11)
INSERT [dbo].[Recetas] ([ID_Receta], [ID_Jefe_de_cocina], [Nombre_receta], [Estado], [descripcion], [categoria], [descripcion_cliente], [ID_sucursal]) VALUES (2110, 1, N'hamburguesa', 1, N'ejemplo', 5, N'ejemplo', 11)
SET IDENTITY_INSERT [dbo].[Recetas] OFF
GO
SET IDENTITY_INSERT [dbo].[recetas_precio_historico] ON 

INSERT [dbo].[recetas_precio_historico] ([ID_Receta_precio_historico], [ID_Receta], [Costo], [Fecha_inicio], [Fecha_Fin]) VALUES (1342, 2104, CAST(1.70 AS Decimal(10, 2)), CAST(N'2025-11-23' AS Date), CAST(N'2025-11-23' AS Date))
INSERT [dbo].[recetas_precio_historico] ([ID_Receta_precio_historico], [ID_Receta], [Costo], [Fecha_inicio], [Fecha_Fin]) VALUES (1343, 2104, CAST(2.15 AS Decimal(10, 2)), CAST(N'2025-11-23' AS Date), CAST(N'2025-11-23' AS Date))
INSERT [dbo].[recetas_precio_historico] ([ID_Receta_precio_historico], [ID_Receta], [Costo], [Fecha_inicio], [Fecha_Fin]) VALUES (1344, 2104, CAST(17.55 AS Decimal(10, 2)), CAST(N'2025-11-23' AS Date), CAST(N'2025-11-28' AS Date))
INSERT [dbo].[recetas_precio_historico] ([ID_Receta_precio_historico], [ID_Receta], [Costo], [Fecha_inicio], [Fecha_Fin]) VALUES (1345, 2105, CAST(3.30 AS Decimal(10, 2)), CAST(N'2025-11-25' AS Date), CAST(N'2025-12-02' AS Date))
INSERT [dbo].[recetas_precio_historico] ([ID_Receta_precio_historico], [ID_Receta], [Costo], [Fecha_inicio], [Fecha_Fin]) VALUES (1346, 2104, CAST(16.05 AS Decimal(10, 2)), CAST(N'2025-11-28' AS Date), CAST(N'2025-11-28' AS Date))
INSERT [dbo].[recetas_precio_historico] ([ID_Receta_precio_historico], [ID_Receta], [Costo], [Fecha_inicio], [Fecha_Fin]) VALUES (1347, 2104, CAST(34.35 AS Decimal(10, 2)), CAST(N'2025-11-28' AS Date), CAST(N'2025-12-02' AS Date))
INSERT [dbo].[recetas_precio_historico] ([ID_Receta_precio_historico], [ID_Receta], [Costo], [Fecha_inicio], [Fecha_Fin]) VALUES (1348, 2104, CAST(34.42 AS Decimal(10, 2)), CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02' AS Date))
INSERT [dbo].[recetas_precio_historico] ([ID_Receta_precio_historico], [ID_Receta], [Costo], [Fecha_inicio], [Fecha_Fin]) VALUES (1349, 2104, CAST(39.07 AS Decimal(10, 2)), CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02' AS Date))
INSERT [dbo].[recetas_precio_historico] ([ID_Receta_precio_historico], [ID_Receta], [Costo], [Fecha_inicio], [Fecha_Fin]) VALUES (1350, 2106, CAST(0.00 AS Decimal(10, 2)), CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02' AS Date))
INSERT [dbo].[recetas_precio_historico] ([ID_Receta_precio_historico], [ID_Receta], [Costo], [Fecha_inicio], [Fecha_Fin]) VALUES (1351, 2106, CAST(2.88 AS Decimal(10, 2)), CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02' AS Date))
INSERT [dbo].[recetas_precio_historico] ([ID_Receta_precio_historico], [ID_Receta], [Costo], [Fecha_inicio], [Fecha_Fin]) VALUES (1352, 2106, CAST(1.73 AS Decimal(10, 2)), CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02' AS Date))
INSERT [dbo].[recetas_precio_historico] ([ID_Receta_precio_historico], [ID_Receta], [Costo], [Fecha_inicio], [Fecha_Fin]) VALUES (1353, 2106, CAST(862.50 AS Decimal(10, 2)), CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02' AS Date))
INSERT [dbo].[recetas_precio_historico] ([ID_Receta_precio_historico], [ID_Receta], [Costo], [Fecha_inicio], [Fecha_Fin]) VALUES (1354, 2106, CAST(920.00 AS Decimal(10, 2)), CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02' AS Date))
INSERT [dbo].[recetas_precio_historico] ([ID_Receta_precio_historico], [ID_Receta], [Costo], [Fecha_inicio], [Fecha_Fin]) VALUES (1355, 2104, CAST(39.40 AS Decimal(10, 2)), CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02' AS Date))
INSERT [dbo].[recetas_precio_historico] ([ID_Receta_precio_historico], [ID_Receta], [Costo], [Fecha_inicio], [Fecha_Fin]) VALUES (1356, 2106, CAST(928.00 AS Decimal(10, 2)), CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02' AS Date))
INSERT [dbo].[recetas_precio_historico] ([ID_Receta_precio_historico], [ID_Receta], [Costo], [Fecha_inicio], [Fecha_Fin]) VALUES (1357, 2104, CAST(39.07 AS Decimal(10, 2)), CAST(N'2025-12-02' AS Date), NULL)
INSERT [dbo].[recetas_precio_historico] ([ID_Receta_precio_historico], [ID_Receta], [Costo], [Fecha_inicio], [Fecha_Fin]) VALUES (1358, 2106, CAST(920.00 AS Decimal(10, 2)), CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02' AS Date))
INSERT [dbo].[recetas_precio_historico] ([ID_Receta_precio_historico], [ID_Receta], [Costo], [Fecha_inicio], [Fecha_Fin]) VALUES (1359, 2106, CAST(920000.00 AS Decimal(10, 2)), CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02' AS Date))
INSERT [dbo].[recetas_precio_historico] ([ID_Receta_precio_historico], [ID_Receta], [Costo], [Fecha_inicio], [Fecha_Fin]) VALUES (1360, 2106, CAST(920.00 AS Decimal(10, 2)), CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02' AS Date))
INSERT [dbo].[recetas_precio_historico] ([ID_Receta_precio_historico], [ID_Receta], [Costo], [Fecha_inicio], [Fecha_Fin]) VALUES (1361, 2106, CAST(920000.00 AS Decimal(10, 2)), CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02' AS Date))
INSERT [dbo].[recetas_precio_historico] ([ID_Receta_precio_historico], [ID_Receta], [Costo], [Fecha_inicio], [Fecha_Fin]) VALUES (1362, 2106, CAST(92.00 AS Decimal(10, 2)), CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02' AS Date))
INSERT [dbo].[recetas_precio_historico] ([ID_Receta_precio_historico], [ID_Receta], [Costo], [Fecha_inicio], [Fecha_Fin]) VALUES (1363, 2106, CAST(18.40 AS Decimal(10, 2)), CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02' AS Date))
INSERT [dbo].[recetas_precio_historico] ([ID_Receta_precio_historico], [ID_Receta], [Costo], [Fecha_inicio], [Fecha_Fin]) VALUES (1364, 2106, CAST(18.70 AS Decimal(10, 2)), CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02' AS Date))
INSERT [dbo].[recetas_precio_historico] ([ID_Receta_precio_historico], [ID_Receta], [Costo], [Fecha_inicio], [Fecha_Fin]) VALUES (1365, 2106, CAST(2244800.30 AS Decimal(10, 2)), CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02' AS Date))
INSERT [dbo].[recetas_precio_historico] ([ID_Receta_precio_historico], [ID_Receta], [Costo], [Fecha_inicio], [Fecha_Fin]) VALUES (1366, 2105, CAST(3.00 AS Decimal(10, 2)), CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02' AS Date))
INSERT [dbo].[recetas_precio_historico] ([ID_Receta_precio_historico], [ID_Receta], [Costo], [Fecha_inicio], [Fecha_Fin]) VALUES (1367, 2105, CAST(6.00 AS Decimal(10, 2)), CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02' AS Date))
INSERT [dbo].[recetas_precio_historico] ([ID_Receta_precio_historico], [ID_Receta], [Costo], [Fecha_inicio], [Fecha_Fin]) VALUES (1368, 2105, CAST(6.70 AS Decimal(10, 2)), CAST(N'2025-12-02' AS Date), NULL)
INSERT [dbo].[recetas_precio_historico] ([ID_Receta_precio_historico], [ID_Receta], [Costo], [Fecha_inicio], [Fecha_Fin]) VALUES (1369, 2106, CAST(140300.30 AS Decimal(10, 2)), CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02' AS Date))
INSERT [dbo].[recetas_precio_historico] ([ID_Receta_precio_historico], [ID_Receta], [Costo], [Fecha_inicio], [Fecha_Fin]) VALUES (1370, 2106, CAST(13420.30 AS Decimal(10, 2)), CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02' AS Date))
INSERT [dbo].[recetas_precio_historico] ([ID_Receta_precio_historico], [ID_Receta], [Costo], [Fecha_inicio], [Fecha_Fin]) VALUES (1371, 2107, CAST(17250000.00 AS Decimal(10, 2)), CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02' AS Date))
INSERT [dbo].[recetas_precio_historico] ([ID_Receta_precio_historico], [ID_Receta], [Costo], [Fecha_inicio], [Fecha_Fin]) VALUES (1372, 2106, CAST(13.72 AS Decimal(10, 2)), CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02' AS Date))
INSERT [dbo].[recetas_precio_historico] ([ID_Receta_precio_historico], [ID_Receta], [Costo], [Fecha_inicio], [Fecha_Fin]) VALUES (1373, 2107, CAST(1725000.00 AS Decimal(10, 2)), CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02' AS Date))
INSERT [dbo].[recetas_precio_historico] ([ID_Receta_precio_historico], [ID_Receta], [Costo], [Fecha_inicio], [Fecha_Fin]) VALUES (1374, 2107, CAST(1725.00 AS Decimal(10, 2)), CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02' AS Date))
INSERT [dbo].[recetas_precio_historico] ([ID_Receta_precio_historico], [ID_Receta], [Costo], [Fecha_inicio], [Fecha_Fin]) VALUES (1375, 2107, CAST(1725000.00 AS Decimal(10, 2)), CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02' AS Date))
INSERT [dbo].[recetas_precio_historico] ([ID_Receta_precio_historico], [ID_Receta], [Costo], [Fecha_inicio], [Fecha_Fin]) VALUES (1376, 2107, CAST(575.00 AS Decimal(10, 2)), CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02' AS Date))
INSERT [dbo].[recetas_precio_historico] ([ID_Receta_precio_historico], [ID_Receta], [Costo], [Fecha_inicio], [Fecha_Fin]) VALUES (1377, 2106, CAST(2104.80 AS Decimal(10, 2)), CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02' AS Date))
INSERT [dbo].[recetas_precio_historico] ([ID_Receta_precio_historico], [ID_Receta], [Costo], [Fecha_inicio], [Fecha_Fin]) VALUES (1378, 2106, CAST(2104500.30 AS Decimal(10, 2)), CAST(N'2025-12-02' AS Date), CAST(N'2025-12-02' AS Date))
INSERT [dbo].[recetas_precio_historico] ([ID_Receta_precio_historico], [ID_Receta], [Costo], [Fecha_inicio], [Fecha_Fin]) VALUES (1379, 2106, CAST(2.40 AS Decimal(10, 2)), CAST(N'2025-12-02' AS Date), CAST(N'2025-12-13' AS Date))
INSERT [dbo].[recetas_precio_historico] ([ID_Receta_precio_historico], [ID_Receta], [Costo], [Fecha_inicio], [Fecha_Fin]) VALUES (1380, 2107, CAST(0.58 AS Decimal(10, 2)), CAST(N'2025-12-02' AS Date), CAST(N'2025-12-03' AS Date))
INSERT [dbo].[recetas_precio_historico] ([ID_Receta_precio_historico], [ID_Receta], [Costo], [Fecha_inicio], [Fecha_Fin]) VALUES (1381, 2107, CAST(86.00 AS Decimal(10, 2)), CAST(N'2025-12-03' AS Date), NULL)
INSERT [dbo].[recetas_precio_historico] ([ID_Receta_precio_historico], [ID_Receta], [Costo], [Fecha_inicio], [Fecha_Fin]) VALUES (1382, 2108, CAST(21.66 AS Decimal(10, 2)), CAST(N'2025-12-13' AS Date), NULL)
INSERT [dbo].[recetas_precio_historico] ([ID_Receta_precio_historico], [ID_Receta], [Costo], [Fecha_inicio], [Fecha_Fin]) VALUES (1383, 2109, CAST(29.40 AS Decimal(10, 2)), CAST(N'2025-12-13' AS Date), NULL)
INSERT [dbo].[recetas_precio_historico] ([ID_Receta_precio_historico], [ID_Receta], [Costo], [Fecha_inicio], [Fecha_Fin]) VALUES (1384, 2110, CAST(12.46 AS Decimal(10, 2)), CAST(N'2025-12-13' AS Date), NULL)
INSERT [dbo].[recetas_precio_historico] ([ID_Receta_precio_historico], [ID_Receta], [Costo], [Fecha_inicio], [Fecha_Fin]) VALUES (2382, 2106, CAST(2.03 AS Decimal(10, 2)), CAST(N'2025-12-13' AS Date), NULL)
SET IDENTITY_INSERT [dbo].[recetas_precio_historico] OFF
GO
SET IDENTITY_INSERT [dbo].[Sucursales] ON 

INSERT [dbo].[Sucursales] ([ID_sucursal], [Descripcion], [ID_Direccion], [estado]) VALUES (1, N'sucursal principal', 1, 1)
INSERT [dbo].[Sucursales] ([ID_sucursal], [Descripcion], [ID_Direccion], [estado]) VALUES (9, N'hol', 1007, 1)
INSERT [dbo].[Sucursales] ([ID_sucursal], [Descripcion], [ID_Direccion], [estado]) VALUES (10, N'sucursal secundaria', 1008, 1)
INSERT [dbo].[Sucursales] ([ID_sucursal], [Descripcion], [ID_Direccion], [estado]) VALUES (11, N'sucursal digital', 1013, 1)
SET IDENTITY_INSERT [dbo].[Sucursales] OFF
GO
SET IDENTITY_INSERT [dbo].[Tipo_documentos] ON 

INSERT [dbo].[Tipo_documentos] ([tipo_doc], [descripcion], [tipo], [numero_documento]) VALUES (3, N'rtn', 2, N'8012005095147')
INSERT [dbo].[Tipo_documentos] ([tipo_doc], [descripcion], [tipo], [numero_documento]) VALUES (4, N'rtn', 2, N'08012005095147')
INSERT [dbo].[Tipo_documentos] ([tipo_doc], [descripcion], [tipo], [numero_documento]) VALUES (5, N'rtn', 2, N'08012005095147')
INSERT [dbo].[Tipo_documentos] ([tipo_doc], [descripcion], [tipo], [numero_documento]) VALUES (6, N'rtn', 2, N'08012005095148')
INSERT [dbo].[Tipo_documentos] ([tipo_doc], [descripcion], [tipo], [numero_documento]) VALUES (7, N'dni', 1, N'08012005095122')
INSERT [dbo].[Tipo_documentos] ([tipo_doc], [descripcion], [tipo], [numero_documento]) VALUES (8, N'dni', 1, N'08012005890')
INSERT [dbo].[Tipo_documentos] ([tipo_doc], [descripcion], [tipo], [numero_documento]) VALUES (9, N'dni', 1, N'08012005095123')
INSERT [dbo].[Tipo_documentos] ([tipo_doc], [descripcion], [tipo], [numero_documento]) VALUES (10, N'dni', 1, N'08012005088432')
INSERT [dbo].[Tipo_documentos] ([tipo_doc], [descripcion], [tipo], [numero_documento]) VALUES (11, N'rtn', 4, N'0801200509000')
INSERT [dbo].[Tipo_documentos] ([tipo_doc], [descripcion], [tipo], [numero_documento]) VALUES (12, N'dni', 1, N'08012005095111')
INSERT [dbo].[Tipo_documentos] ([tipo_doc], [descripcion], [tipo], [numero_documento]) VALUES (13, N'dni', 1, N'08012005090211')
INSERT [dbo].[Tipo_documentos] ([tipo_doc], [descripcion], [tipo], [numero_documento]) VALUES (14, N'dni', 1, N'08012005022222')
INSERT [dbo].[Tipo_documentos] ([tipo_doc], [descripcion], [tipo], [numero_documento]) VALUES (15, N'dni', 1, N'08012065012143')
INSERT [dbo].[Tipo_documentos] ([tipo_doc], [descripcion], [tipo], [numero_documento]) VALUES (16, N'dni', 1, N'0505250509505')
INSERT [dbo].[Tipo_documentos] ([tipo_doc], [descripcion], [tipo], [numero_documento]) VALUES (17, N'dni', 1, N'08012005076543')
SET IDENTITY_INSERT [dbo].[Tipo_documentos] OFF
GO
INSERT [dbo].[Unidades_Conversion] ([ID_Unidad], [Nombre_Unidad], [Equivalente], [Tipo]) VALUES (1, N'Kilogramo', CAST(1000.0000 AS Decimal(10, 4)), 1)
INSERT [dbo].[Unidades_Conversion] ([ID_Unidad], [Nombre_Unidad], [Equivalente], [Tipo]) VALUES (2, N'Gramo', CAST(1.0000 AS Decimal(10, 4)), 1)
INSERT [dbo].[Unidades_Conversion] ([ID_Unidad], [Nombre_Unidad], [Equivalente], [Tipo]) VALUES (3, N'Libra', CAST(453.5920 AS Decimal(10, 4)), 1)
INSERT [dbo].[Unidades_Conversion] ([ID_Unidad], [Nombre_Unidad], [Equivalente], [Tipo]) VALUES (5, N'Miligramo', CAST(0.0010 AS Decimal(10, 4)), 1)
INSERT [dbo].[Unidades_Conversion] ([ID_Unidad], [Nombre_Unidad], [Equivalente], [Tipo]) VALUES (6, N'Litro', CAST(1000.0000 AS Decimal(10, 4)), 2)
INSERT [dbo].[Unidades_Conversion] ([ID_Unidad], [Nombre_Unidad], [Equivalente], [Tipo]) VALUES (7, N'Mililitro', CAST(1.0000 AS Decimal(10, 4)), 2)
GO
SET IDENTITY_INSERT [dbo].[Unidades_medida] ON 

INSERT [dbo].[Unidades_medida] ([ID_Unidad], [Nombre], [abreviatura], [Tipo]) VALUES (1, N'Kilogramo', N'kg', 1)
INSERT [dbo].[Unidades_medida] ([ID_Unidad], [Nombre], [abreviatura], [Tipo]) VALUES (2, N'Gramo', N'g', 1)
INSERT [dbo].[Unidades_medida] ([ID_Unidad], [Nombre], [abreviatura], [Tipo]) VALUES (3, N'Libra', N'lb', 1)
INSERT [dbo].[Unidades_medida] ([ID_Unidad], [Nombre], [abreviatura], [Tipo]) VALUES (4, N'Onza', N'oz', 1)
INSERT [dbo].[Unidades_medida] ([ID_Unidad], [Nombre], [abreviatura], [Tipo]) VALUES (5, N'Miligramo', N'mg', 1)
INSERT [dbo].[Unidades_medida] ([ID_Unidad], [Nombre], [abreviatura], [Tipo]) VALUES (6, N'Litro', N'L', 2)
INSERT [dbo].[Unidades_medida] ([ID_Unidad], [Nombre], [abreviatura], [Tipo]) VALUES (7, N'Mililitro', N'mL', 2)
INSERT [dbo].[Unidades_medida] ([ID_Unidad], [Nombre], [abreviatura], [Tipo]) VALUES (8, N'Unidad', N'u', 3)
INSERT [dbo].[Unidades_medida] ([ID_Unidad], [Nombre], [abreviatura], [Tipo]) VALUES (9, N'Paquete', N'paq', 3)
INSERT [dbo].[Unidades_medida] ([ID_Unidad], [Nombre], [abreviatura], [Tipo]) VALUES (19, N'Ewqrsadwq', N'PEWQ', 1)
SET IDENTITY_INSERT [dbo].[Unidades_medida] OFF
GO
SET IDENTITY_INSERT [dbo].[Usuarios_cliente] ON 

INSERT [dbo].[Usuarios_cliente] ([ID_Usuario_ClienteF], [Username], [password], [nombre], [apellido], [telefono], [ID_sucursal], [estado], [correo]) VALUES (1, N'kevin_herrera', N'$2b$12$A3Nkw17B8Rfw3NJ/MQ6CAOlUdKBmm3B.Zqf71u4ay/j2JsS7bOF4W', N'Kevin Alejandro', N'Herrera Guillen', N'99827720', 11, 1, NULL)
INSERT [dbo].[Usuarios_cliente] ([ID_Usuario_ClienteF], [Username], [password], [nombre], [apellido], [telefono], [ID_sucursal], [estado], [correo]) VALUES (1001, N'kevin', N'K3v!n190305', N'Kevive', N'Herrera Guillen', N'99827720', 11, 1, NULL)
INSERT [dbo].[Usuarios_cliente] ([ID_Usuario_ClienteF], [Username], [password], [nombre], [apellido], [telefono], [ID_sucursal], [estado], [correo]) VALUES (1002, N'ejemplo', N'$2b$12$sJdjWlYp8MK7Sj0UH7W/UOfipk3QmmLfuKKqfHRHKjPPp2Bm3wa9S', N'Ejemplo', N'Ejemplo Yo', N'99827723', 11, 1, NULL)
INSERT [dbo].[Usuarios_cliente] ([ID_Usuario_ClienteF], [Username], [password], [nombre], [apellido], [telefono], [ID_sucursal], [estado], [correo]) VALUES (1003, N'dwqdqw', N'$2b$12$gJSls.BOAWlmNbztoFLpx..xG7XhRhi7LUbG.VmN6YvlCi33LFMaK', N'Dsadsa', N'Dasads', N'99821111', 11, 1, N'kevin.herrera2@ujcv.edu.hn')
SET IDENTITY_INSERT [dbo].[Usuarios_cliente] OFF
GO
SET ANSI_PADDING ON
GO
/****** Object:  Index [auth_group_name_a6ea08ec_uniq]    Script Date: 2/2/2026 09:13:33 p. m. ******/
ALTER TABLE [dbo].[auth_group] ADD  CONSTRAINT [auth_group_name_a6ea08ec_uniq] UNIQUE NONCLUSTERED 
(
	[name] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
/****** Object:  Index [auth_group_permissions_group_id_b120cbf9]    Script Date: 2/2/2026 09:13:33 p. m. ******/
CREATE NONCLUSTERED INDEX [auth_group_permissions_group_id_b120cbf9] ON [dbo].[auth_group_permissions]
(
	[group_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
/****** Object:  Index [auth_group_permissions_group_id_permission_id_0cd325b0_uniq]    Script Date: 2/2/2026 09:13:33 p. m. ******/
CREATE UNIQUE NONCLUSTERED INDEX [auth_group_permissions_group_id_permission_id_0cd325b0_uniq] ON [dbo].[auth_group_permissions]
(
	[group_id] ASC,
	[permission_id] ASC
)
WHERE ([group_id] IS NOT NULL AND [permission_id] IS NOT NULL)
WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
/****** Object:  Index [auth_group_permissions_permission_id_84c5c92e]    Script Date: 2/2/2026 09:13:33 p. m. ******/
CREATE NONCLUSTERED INDEX [auth_group_permissions_permission_id_84c5c92e] ON [dbo].[auth_group_permissions]
(
	[permission_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
/****** Object:  Index [auth_permission_content_type_id_2f476e4b]    Script Date: 2/2/2026 09:13:33 p. m. ******/
CREATE NONCLUSTERED INDEX [auth_permission_content_type_id_2f476e4b] ON [dbo].[auth_permission]
(
	[content_type_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
SET ANSI_PADDING ON
GO
/****** Object:  Index [auth_permission_content_type_id_codename_01ab375a_uniq]    Script Date: 2/2/2026 09:13:33 p. m. ******/
CREATE UNIQUE NONCLUSTERED INDEX [auth_permission_content_type_id_codename_01ab375a_uniq] ON [dbo].[auth_permission]
(
	[content_type_id] ASC,
	[codename] ASC
)
WHERE ([content_type_id] IS NOT NULL AND [codename] IS NOT NULL)
WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
SET ANSI_PADDING ON
GO
/****** Object:  Index [auth_user_username_6821ab7c_uniq]    Script Date: 2/2/2026 09:13:33 p. m. ******/
ALTER TABLE [dbo].[auth_user] ADD  CONSTRAINT [auth_user_username_6821ab7c_uniq] UNIQUE NONCLUSTERED 
(
	[username] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
/****** Object:  Index [auth_user_groups_group_id_97559544]    Script Date: 2/2/2026 09:13:33 p. m. ******/
CREATE NONCLUSTERED INDEX [auth_user_groups_group_id_97559544] ON [dbo].[auth_user_groups]
(
	[group_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
/****** Object:  Index [auth_user_groups_user_id_6a12ed8b]    Script Date: 2/2/2026 09:13:33 p. m. ******/
CREATE NONCLUSTERED INDEX [auth_user_groups_user_id_6a12ed8b] ON [dbo].[auth_user_groups]
(
	[user_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
/****** Object:  Index [auth_user_groups_user_id_group_id_94350c0c_uniq]    Script Date: 2/2/2026 09:13:33 p. m. ******/
CREATE UNIQUE NONCLUSTERED INDEX [auth_user_groups_user_id_group_id_94350c0c_uniq] ON [dbo].[auth_user_groups]
(
	[user_id] ASC,
	[group_id] ASC
)
WHERE ([user_id] IS NOT NULL AND [group_id] IS NOT NULL)
WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
/****** Object:  Index [auth_user_user_permissions_permission_id_1fbb5f2c]    Script Date: 2/2/2026 09:13:33 p. m. ******/
CREATE NONCLUSTERED INDEX [auth_user_user_permissions_permission_id_1fbb5f2c] ON [dbo].[auth_user_user_permissions]
(
	[permission_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
/****** Object:  Index [auth_user_user_permissions_user_id_a95ead1b]    Script Date: 2/2/2026 09:13:33 p. m. ******/
CREATE NONCLUSTERED INDEX [auth_user_user_permissions_user_id_a95ead1b] ON [dbo].[auth_user_user_permissions]
(
	[user_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
/****** Object:  Index [auth_user_user_permissions_user_id_permission_id_14a6b632_uniq]    Script Date: 2/2/2026 09:13:33 p. m. ******/
CREATE UNIQUE NONCLUSTERED INDEX [auth_user_user_permissions_user_id_permission_id_14a6b632_uniq] ON [dbo].[auth_user_user_permissions]
(
	[user_id] ASC,
	[permission_id] ASC
)
WHERE ([user_id] IS NOT NULL AND [permission_id] IS NOT NULL)
WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
/****** Object:  Index [IXFK_CAI_Sucursales]    Script Date: 2/2/2026 09:13:33 p. m. ******/
CREATE NONCLUSTERED INDEX [IXFK_CAI_Sucursales] ON [dbo].[CAI]
(
	[ID_sucursal] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
/****** Object:  Index [IXFK_clientes_documento_Usuarios_cliente]    Script Date: 2/2/2026 09:13:33 p. m. ******/
CREATE NONCLUSTERED INDEX [IXFK_clientes_documento_Usuarios_cliente] ON [dbo].[clientes_documento]
(
	[ID_Usuario_ClienteF] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
/****** Object:  Index [IXFK_Detalles_de_pago_Pagos]    Script Date: 2/2/2026 09:13:33 p. m. ******/
CREATE NONCLUSTERED INDEX [IXFK_Detalles_de_pago_Pagos] ON [dbo].[Detalles_de_pago]
(
	[ID_Pago] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
/****** Object:  Index [IXFK_Detalles_de_pago_Tipo_De_Pago]    Script Date: 2/2/2026 09:13:33 p. m. ******/
CREATE NONCLUSTERED INDEX [IXFK_Detalles_de_pago_Tipo_De_Pago] ON [dbo].[Detalles_de_pago]
(
	[ID_Tipo_De_Pago] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
/****** Object:  Index [IXFK_Direccion_de_los_proveedores_Proveedores]    Script Date: 2/2/2026 09:13:33 p. m. ******/
CREATE NONCLUSTERED INDEX [IXFK_Direccion_de_los_proveedores_Proveedores] ON [dbo].[Direccion_de_los_proveedores]
(
	[ID_Proveedor] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
/****** Object:  Index [IXFK_Direccion_del_cliente_Direcciones]    Script Date: 2/2/2026 09:13:33 p. m. ******/
CREATE NONCLUSTERED INDEX [IXFK_Direccion_del_cliente_Direcciones] ON [dbo].[Direccion_del_cliente]
(
	[ID_Direccion] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
/****** Object:  Index [django_admin_log_content_type_id_c4bce8eb]    Script Date: 2/2/2026 09:13:33 p. m. ******/
CREATE NONCLUSTERED INDEX [django_admin_log_content_type_id_c4bce8eb] ON [dbo].[django_admin_log]
(
	[content_type_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
/****** Object:  Index [django_admin_log_user_id_c564eba6]    Script Date: 2/2/2026 09:13:33 p. m. ******/
CREATE NONCLUSTERED INDEX [django_admin_log_user_id_c564eba6] ON [dbo].[django_admin_log]
(
	[user_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
SET ANSI_PADDING ON
GO
/****** Object:  Index [django_content_type_app_label_model_76bd3d3b_uniq]    Script Date: 2/2/2026 09:13:33 p. m. ******/
CREATE UNIQUE NONCLUSTERED INDEX [django_content_type_app_label_model_76bd3d3b_uniq] ON [dbo].[django_content_type]
(
	[app_label] ASC,
	[model] ASC
)
WHERE ([app_label] IS NOT NULL AND [model] IS NOT NULL)
WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
/****** Object:  Index [django_session_expire_date_a5c62663]    Script Date: 2/2/2026 09:13:33 p. m. ******/
CREATE NONCLUSTERED INDEX [django_session_expire_date_a5c62663] ON [dbo].[django_session]
(
	[expire_date] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
SET ANSI_PADDING ON
GO
/****** Object:  Index [UQ__Empleado__536C85E401BBCEB8]    Script Date: 2/2/2026 09:13:33 p. m. ******/
ALTER TABLE [dbo].[Empleado] ADD UNIQUE NONCLUSTERED 
(
	[Username] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
SET ANSI_PADDING ON
GO
/****** Object:  Index [IX_Empleado_Email]    Script Date: 2/2/2026 09:13:33 p. m. ******/
CREATE UNIQUE NONCLUSTERED INDEX [IX_Empleado_Email] ON [dbo].[Empleado]
(
	[Email] ASC
)
WHERE ([Email] IS NOT NULL)
WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
/****** Object:  Index [IXFK_Empleado_documento_Tipo_documento]    Script Date: 2/2/2026 09:13:33 p. m. ******/
CREATE NONCLUSTERED INDEX [IXFK_Empleado_documento_Tipo_documento] ON [dbo].[Empleado_documento]
(
	[tipo_doc] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
/****** Object:  Index [IX_Facturas_ID_Usuario_ClienteF]    Script Date: 2/2/2026 09:13:33 p. m. ******/
CREATE NONCLUSTERED INDEX [IX_Facturas_ID_Usuario_ClienteF] ON [dbo].[Facturas]
(
	[ID_Usuario_ClienteF] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
/****** Object:  Index [UQ_historial_ordenes_repartidor_orden]    Script Date: 2/2/2026 09:13:33 p. m. ******/
ALTER TABLE [dbo].[historial_ordenes_repartidor] ADD  CONSTRAINT [UQ_historial_ordenes_repartidor_orden] UNIQUE NONCLUSTERED 
(
	[ID_Orden] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
/****** Object:  Index [IXFK_IM_FA_Facturas]    Script Date: 2/2/2026 09:13:33 p. m. ******/
CREATE NONCLUSTERED INDEX [IXFK_IM_FA_Facturas] ON [dbo].[IM_FA]
(
	[ID_Parametro] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
/****** Object:  Index [IXFK_IM_FA_Impuestos]    Script Date: 2/2/2026 09:13:33 p. m. ******/
CREATE NONCLUSTERED INDEX [IXFK_IM_FA_Impuestos] ON [dbo].[IM_FA]
(
	[ID_Impuesto] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
/****** Object:  Index [IXFK_IN_RE_Insumos]    Script Date: 2/2/2026 09:13:33 p. m. ******/
CREATE NONCLUSTERED INDEX [IXFK_IN_RE_Insumos] ON [dbo].[IN_RE]
(
	[ID_Insumo] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
/****** Object:  Index [IXFK_Insumo_Precio_historico_Insumos]    Script Date: 2/2/2026 09:13:33 p. m. ******/
CREATE NONCLUSTERED INDEX [IXFK_Insumo_Precio_historico_Insumos] ON [dbo].[Insumo_Precio_historico]
(
	[ID_Insumo] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
/****** Object:  Index [IXFK_Orden_Compra_a_los_Proveedores_Facturas]    Script Date: 2/2/2026 09:13:33 p. m. ******/
CREATE NONCLUSTERED INDEX [IXFK_Orden_Compra_a_los_Proveedores_Facturas] ON [dbo].[Orden_Compra_a_los_Proveedores]
(
	[ID_Parametro] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
/****** Object:  Index [IXFK_Orden_Compra_a_los_Proveedores_Insumos]    Script Date: 2/2/2026 09:13:33 p. m. ******/
CREATE NONCLUSTERED INDEX [IXFK_Orden_Compra_a_los_Proveedores_Insumos] ON [dbo].[Orden_Compra_a_los_Proveedores]
(
	[ID_Insumo] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
/****** Object:  Index [IXFK_Orden_Compra_a_los_Proveedores_Proveedores]    Script Date: 2/2/2026 09:13:33 p. m. ******/
CREATE NONCLUSTERED INDEX [IXFK_Orden_Compra_a_los_Proveedores_Proveedores] ON [dbo].[Orden_Compra_a_los_Proveedores]
(
	[ID_Proveedor] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
SET ANSI_PADDING ON
GO
/****** Object:  Index [UQ__Parametr__4928AC4F39D989BD]    Script Date: 2/2/2026 09:13:33 p. m. ******/
ALTER TABLE [dbo].[Parametros_SAR] ADD UNIQUE NONCLUSTERED 
(
	[Parametro] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
/****** Object:  Index [IXFK_Proveedor_documento_Proveedores]    Script Date: 2/2/2026 09:13:33 p. m. ******/
CREATE NONCLUSTERED INDEX [IXFK_Proveedor_documento_Proveedores] ON [dbo].[Proveedor_documento]
(
	[ID_Proveedor] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
/****** Object:  Index [IXFK_Proveedor_documento_Tipo_documentos]    Script Date: 2/2/2026 09:13:33 p. m. ******/
CREATE NONCLUSTERED INDEX [IXFK_Proveedor_documento_Tipo_documentos] ON [dbo].[Proveedor_documento]
(
	[tipo_doc] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
/****** Object:  Index [UQ_Proveedor_Insumo_Proveedor_Insumo]    Script Date: 2/2/2026 09:13:33 p. m. ******/
ALTER TABLE [dbo].[Proveedor_Insumo] ADD  CONSTRAINT [UQ_Proveedor_Insumo_Proveedor_Insumo] UNIQUE NONCLUSTERED 
(
	[ID_Proveedor] ASC,
	[ID_Insumo] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
SET ANSI_PADDING ON
GO
/****** Object:  Index [UQ__Puesto__055C5F24D24CBBE2]    Script Date: 2/2/2026 09:13:33 p. m. ******/
ALTER TABLE [dbo].[Puesto] ADD UNIQUE NONCLUSTERED 
(
	[Nombre_Puesto] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
/****** Object:  Index [IXFK_Sucursales_Direcciones]    Script Date: 2/2/2026 09:13:33 p. m. ******/
CREATE NONCLUSTERED INDEX [IXFK_Sucursales_Direcciones] ON [dbo].[Sucursales]
(
	[ID_Direccion] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
SET ANSI_PADDING ON
GO
/****** Object:  Index [UX_Usuarios_cliente_correo]    Script Date: 2/2/2026 09:13:33 p. m. ******/
CREATE UNIQUE NONCLUSTERED INDEX [UX_Usuarios_cliente_correo] ON [dbo].[Usuarios_cliente]
(
	[correo] ASC
)
WHERE ([correo] IS NOT NULL AND [correo]<>'')
WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
ALTER TABLE [dbo].[CAI] ADD  DEFAULT ((1)) FOR [estado]
GO
ALTER TABLE [dbo].[CAI_Historico] ADD  DEFAULT (getdate()) FOR [Fecha_Registro]
GO
ALTER TABLE [dbo].[Carrito] ADD  DEFAULT ((1)) FOR [Cantidad]
GO
ALTER TABLE [dbo].[categorias] ADD  CONSTRAINT [DF_categorias_tipo]  DEFAULT ((1)) FOR [tipo]
GO
ALTER TABLE [dbo].[cocineros] ADD  DEFAULT ((1)) FOR [ID_sucursal]
GO
ALTER TABLE [dbo].[Empleado] ADD  CONSTRAINT [DF_Empleado_estado]  DEFAULT ((1)) FOR [estado]
GO
ALTER TABLE [dbo].[Facturas] ADD  DEFAULT ((0)) FOR [Descuento]
GO
ALTER TABLE [dbo].[Facturas] ADD  DEFAULT ((0)) FOR [Impuesto]
GO
ALTER TABLE [dbo].[historial_ordenes_repartidor] ADD  CONSTRAINT [DF_historial_ordenes_repartidor_fecha]  DEFAULT (sysutcdatetime()) FOR [Fecha_Finalizacion]
GO
ALTER TABLE [dbo].[Impuesto_Categoria] ADD  DEFAULT ((1)) FOR [Activo]
GO
ALTER TABLE [dbo].[Impuesto_tasa_historica] ADD  CONSTRAINT [DF_ImpTasaHist_FechaIni]  DEFAULT (getdate()) FOR [fecha_inicio]
GO
ALTER TABLE [dbo].[IN_RE] ADD  CONSTRAINT [DF_IN_RE_Activo]  DEFAULT ((1)) FOR [Activo]
GO
ALTER TABLE [dbo].[IN_RE] ADD  DEFAULT ((0)) FOR [cantidad_usada]
GO
ALTER TABLE [dbo].[IN_RE] ADD  CONSTRAINT [DF_IN_RE_ID_sucursal]  DEFAULT ((11)) FOR [ID_sucursal]
GO
ALTER TABLE [dbo].[Insumos] ADD  CONSTRAINT [DF_Insumos_ID_sucursal]  DEFAULT ((11)) FOR [ID_sucursal]
GO
ALTER TABLE [dbo].[Jefe_de_cocina] ADD  DEFAULT ((1)) FOR [ID_sucursal]
GO
ALTER TABLE [dbo].[Orden_Entrega] ADD  CONSTRAINT [DF_Orden_Entrega_estado]  DEFAULT ((0)) FOR [estado]
GO
ALTER TABLE [dbo].[Orden_Entrega] ADD  CONSTRAINT [DF_Orden_Entrega_Fecha_Creacion]  DEFAULT (getdate()) FOR [Fecha_Creacion]
GO
ALTER TABLE [dbo].[Ordenes_Proveedores] ADD  CONSTRAINT [DF_OrdenesProv_FechaInicio]  DEFAULT (sysdatetime()) FOR [Fecha_Inicio]
GO
ALTER TABLE [dbo].[Ordenes_Proveedores] ADD  CONSTRAINT [DF_OrdenesProv_Estado]  DEFAULT ((0)) FOR [Estado]
GO
ALTER TABLE [dbo].[Ordenes_Proveedores] ADD  CONSTRAINT [DF_Ordenes_Proveedores_Inventario_Aplicado]  DEFAULT ((0)) FOR [Inventario_Aplicado]
GO
ALTER TABLE [dbo].[Proveedor_Insumo] ADD  DEFAULT ((1)) FOR [Activo]
GO
ALTER TABLE [dbo].[Puesto] ADD  CONSTRAINT [DF_Puesto_estado]  DEFAULT ((1)) FOR [estado]
GO
ALTER TABLE [dbo].[Recetas] ADD  CONSTRAINT [DF_Recetas_ID_sucursal]  DEFAULT ((11)) FOR [ID_sucursal]
GO
ALTER TABLE [dbo].[Sucursales] ADD  CONSTRAINT [DF_Sucursales_estado]  DEFAULT ((1)) FOR [estado]
GO
ALTER TABLE [dbo].[Usuarios_cliente] ADD  DEFAULT ((1)) FOR [estado]
GO
ALTER TABLE [dbo].[auth_group_permissions]  WITH CHECK ADD  CONSTRAINT [auth_group_permissions_group_id_b120cbf9_fk_auth_group_id] FOREIGN KEY([group_id])
REFERENCES [dbo].[auth_group] ([id])
GO
ALTER TABLE [dbo].[auth_group_permissions] CHECK CONSTRAINT [auth_group_permissions_group_id_b120cbf9_fk_auth_group_id]
GO
ALTER TABLE [dbo].[auth_group_permissions]  WITH CHECK ADD  CONSTRAINT [auth_group_permissions_permission_id_84c5c92e_fk_auth_permission_id] FOREIGN KEY([permission_id])
REFERENCES [dbo].[auth_permission] ([id])
GO
ALTER TABLE [dbo].[auth_group_permissions] CHECK CONSTRAINT [auth_group_permissions_permission_id_84c5c92e_fk_auth_permission_id]
GO
ALTER TABLE [dbo].[auth_permission]  WITH CHECK ADD  CONSTRAINT [auth_permission_content_type_id_2f476e4b_fk_django_content_type_id] FOREIGN KEY([content_type_id])
REFERENCES [dbo].[django_content_type] ([id])
GO
ALTER TABLE [dbo].[auth_permission] CHECK CONSTRAINT [auth_permission_content_type_id_2f476e4b_fk_django_content_type_id]
GO
ALTER TABLE [dbo].[auth_user_groups]  WITH CHECK ADD  CONSTRAINT [auth_user_groups_group_id_97559544_fk_auth_group_id] FOREIGN KEY([group_id])
REFERENCES [dbo].[auth_group] ([id])
GO
ALTER TABLE [dbo].[auth_user_groups] CHECK CONSTRAINT [auth_user_groups_group_id_97559544_fk_auth_group_id]
GO
ALTER TABLE [dbo].[auth_user_groups]  WITH CHECK ADD  CONSTRAINT [auth_user_groups_user_id_6a12ed8b_fk_auth_user_id] FOREIGN KEY([user_id])
REFERENCES [dbo].[auth_user] ([id])
GO
ALTER TABLE [dbo].[auth_user_groups] CHECK CONSTRAINT [auth_user_groups_user_id_6a12ed8b_fk_auth_user_id]
GO
ALTER TABLE [dbo].[auth_user_user_permissions]  WITH CHECK ADD  CONSTRAINT [auth_user_user_permissions_permission_id_1fbb5f2c_fk_auth_permission_id] FOREIGN KEY([permission_id])
REFERENCES [dbo].[auth_permission] ([id])
GO
ALTER TABLE [dbo].[auth_user_user_permissions] CHECK CONSTRAINT [auth_user_user_permissions_permission_id_1fbb5f2c_fk_auth_permission_id]
GO
ALTER TABLE [dbo].[auth_user_user_permissions]  WITH CHECK ADD  CONSTRAINT [auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id] FOREIGN KEY([user_id])
REFERENCES [dbo].[auth_user] ([id])
GO
ALTER TABLE [dbo].[auth_user_user_permissions] CHECK CONSTRAINT [auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id]
GO
ALTER TABLE [dbo].[CAI]  WITH CHECK ADD  CONSTRAINT [FK_CAI_Sucursales] FOREIGN KEY([ID_sucursal])
REFERENCES [dbo].[Sucursales] ([ID_sucursal])
GO
ALTER TABLE [dbo].[CAI] CHECK CONSTRAINT [FK_CAI_Sucursales]
GO
ALTER TABLE [dbo].[CAI_Historico]  WITH CHECK ADD  CONSTRAINT [FK_CAI_Historico_CAI] FOREIGN KEY([ID_Cai])
REFERENCES [dbo].[CAI] ([ID_Cai])
GO
ALTER TABLE [dbo].[CAI_Historico] CHECK CONSTRAINT [FK_CAI_Historico_CAI]
GO
ALTER TABLE [dbo].[Carrito]  WITH CHECK ADD  CONSTRAINT [FK_Carrito_IN_RE] FOREIGN KEY([ID_IN_RE])
REFERENCES [dbo].[IN_RE] ([ID_IN_RE])
GO
ALTER TABLE [dbo].[Carrito] CHECK CONSTRAINT [FK_Carrito_IN_RE]
GO
ALTER TABLE [dbo].[Carrito]  WITH CHECK ADD  CONSTRAINT [FK_Carrito_UsuarioClienteF] FOREIGN KEY([ID_Usuario_ClienteF])
REFERENCES [dbo].[Usuarios_cliente] ([ID_Usuario_ClienteF])
GO
ALTER TABLE [dbo].[Carrito] CHECK CONSTRAINT [FK_Carrito_UsuarioClienteF]
GO
ALTER TABLE [dbo].[clientes_documento]  WITH CHECK ADD  CONSTRAINT [FK_clientes_documento_Usuarios_cliente] FOREIGN KEY([ID_Usuario_ClienteF])
REFERENCES [dbo].[Usuarios_cliente] ([ID_Usuario_ClienteF])
GO
ALTER TABLE [dbo].[clientes_documento] CHECK CONSTRAINT [FK_clientes_documento_Usuarios_cliente]
GO
ALTER TABLE [dbo].[cocineros]  WITH CHECK ADD  CONSTRAINT [FK_cocinero_Jefe_de_cocina] FOREIGN KEY([ID_Jefe_de_cocina])
REFERENCES [dbo].[Jefe_de_cocina] ([ID_Jefe_de_cocina])
GO
ALTER TABLE [dbo].[cocineros] CHECK CONSTRAINT [FK_cocinero_Jefe_de_cocina]
GO
ALTER TABLE [dbo].[cocineros]  WITH CHECK ADD  CONSTRAINT [FK_Cocineros_Sucursal] FOREIGN KEY([ID_sucursal])
REFERENCES [dbo].[Sucursales] ([ID_sucursal])
GO
ALTER TABLE [dbo].[cocineros] CHECK CONSTRAINT [FK_Cocineros_Sucursal]
GO
ALTER TABLE [dbo].[detalle_compra]  WITH CHECK ADD  CONSTRAINT [FK_detalle_compra_Orden_Compra_Al_Proveedor] FOREIGN KEY([ID_CompraP])
REFERENCES [dbo].[Orden_Compra_a_los_Proveedores] ([ID_CompraP])
GO
ALTER TABLE [dbo].[detalle_compra] CHECK CONSTRAINT [FK_detalle_compra_Orden_Compra_Al_Proveedor]
GO
ALTER TABLE [dbo].[Detalle_Venta_Cliente]  WITH CHECK ADD  CONSTRAINT [FK_Detalle_Venta_Cliente_Orden_Cliente] FOREIGN KEY([ID_Orden_cliente])
REFERENCES [dbo].[Orden_Cliente] ([ID_Orden_cliente])
GO
ALTER TABLE [dbo].[Detalle_Venta_Cliente] CHECK CONSTRAINT [FK_Detalle_Venta_Cliente_Orden_Cliente]
GO
ALTER TABLE [dbo].[Detalles_de_pago]  WITH CHECK ADD  CONSTRAINT [FK_Detalles_de_pago_Pagos] FOREIGN KEY([ID_Pago])
REFERENCES [dbo].[Pagos] ([ID_Pago])
GO
ALTER TABLE [dbo].[Detalles_de_pago] CHECK CONSTRAINT [FK_Detalles_de_pago_Pagos]
GO
ALTER TABLE [dbo].[Detalles_de_pago]  WITH CHECK ADD  CONSTRAINT [FK_Detalles_de_pago_Tipo_De_Pago] FOREIGN KEY([ID_Tipo_De_Pago])
REFERENCES [dbo].[Tipo_De_Pago] ([ID_Tipo_De_Pago])
GO
ALTER TABLE [dbo].[Detalles_de_pago] CHECK CONSTRAINT [FK_Detalles_de_pago_Tipo_De_Pago]
GO
ALTER TABLE [dbo].[Direccion_de_los_proveedores]  WITH CHECK ADD  CONSTRAINT [FK_DI_PR_Direccion] FOREIGN KEY([ID_Direccion])
REFERENCES [dbo].[Direcciones] ([ID_Direccion])
GO
ALTER TABLE [dbo].[Direccion_de_los_proveedores] CHECK CONSTRAINT [FK_DI_PR_Direccion]
GO
ALTER TABLE [dbo].[Direccion_de_los_proveedores]  WITH CHECK ADD  CONSTRAINT [FK_Direccion_de_los_proveedores_Proveedores] FOREIGN KEY([ID_Proveedor])
REFERENCES [dbo].[Proveedores] ([ID_Proveedor])
GO
ALTER TABLE [dbo].[Direccion_de_los_proveedores] CHECK CONSTRAINT [FK_Direccion_de_los_proveedores_Proveedores]
GO
ALTER TABLE [dbo].[Direccion_del_cliente]  WITH CHECK ADD  CONSTRAINT [FK_Direccion_del_cliente_Direcciones] FOREIGN KEY([ID_Direccion])
REFERENCES [dbo].[Direcciones] ([ID_Direccion])
GO
ALTER TABLE [dbo].[Direccion_del_cliente] CHECK CONSTRAINT [FK_Direccion_del_cliente_Direcciones]
GO
ALTER TABLE [dbo].[Direccion_del_cliente]  WITH CHECK ADD  CONSTRAINT [FK_US_CO_Usuario_cliente] FOREIGN KEY([ID_Usuario_ClienteF])
REFERENCES [dbo].[Usuarios_cliente] ([ID_Usuario_ClienteF])
GO
ALTER TABLE [dbo].[Direccion_del_cliente] CHECK CONSTRAINT [FK_US_CO_Usuario_cliente]
GO
ALTER TABLE [dbo].[Direccion_del_empleado]  WITH CHECK ADD  CONSTRAINT [FK_DirEmp_Direcciones] FOREIGN KEY([ID_Direccion])
REFERENCES [dbo].[Direcciones] ([ID_Direccion])
GO
ALTER TABLE [dbo].[Direccion_del_empleado] CHECK CONSTRAINT [FK_DirEmp_Direcciones]
GO
ALTER TABLE [dbo].[Direccion_del_empleado]  WITH CHECK ADD  CONSTRAINT [FK_DirEmp_Empleado] FOREIGN KEY([ID_Empleado])
REFERENCES [dbo].[Empleado] ([ID_Empleado])
GO
ALTER TABLE [dbo].[Direccion_del_empleado] CHECK CONSTRAINT [FK_DirEmp_Empleado]
GO
ALTER TABLE [dbo].[django_admin_log]  WITH CHECK ADD  CONSTRAINT [django_admin_log_content_type_id_c4bce8eb_fk_django_content_type_id] FOREIGN KEY([content_type_id])
REFERENCES [dbo].[django_content_type] ([id])
GO
ALTER TABLE [dbo].[django_admin_log] CHECK CONSTRAINT [django_admin_log_content_type_id_c4bce8eb_fk_django_content_type_id]
GO
ALTER TABLE [dbo].[django_admin_log]  WITH CHECK ADD  CONSTRAINT [django_admin_log_user_id_c564eba6_fk_auth_user_id] FOREIGN KEY([user_id])
REFERENCES [dbo].[auth_user] ([id])
GO
ALTER TABLE [dbo].[django_admin_log] CHECK CONSTRAINT [django_admin_log_user_id_c564eba6_fk_auth_user_id]
GO
ALTER TABLE [dbo].[Empleado]  WITH CHECK ADD  CONSTRAINT [FK_Empleado_Puesto] FOREIGN KEY([ID_Puesto])
REFERENCES [dbo].[Puesto] ([ID_Puesto])
GO
ALTER TABLE [dbo].[Empleado] CHECK CONSTRAINT [FK_Empleado_Puesto]
GO
ALTER TABLE [dbo].[Empleado]  WITH CHECK ADD  CONSTRAINT [FK_Empleado_Sucursal] FOREIGN KEY([ID_sucursal])
REFERENCES [dbo].[Sucursales] ([ID_sucursal])
GO
ALTER TABLE [dbo].[Empleado] CHECK CONSTRAINT [FK_Empleado_Sucursal]
GO
ALTER TABLE [dbo].[Empleado_documento]  WITH CHECK ADD  CONSTRAINT [FK_Empleado_documento_Tipo_documento] FOREIGN KEY([tipo_doc])
REFERENCES [dbo].[Tipo_documentos] ([tipo_doc])
GO
ALTER TABLE [dbo].[Empleado_documento] CHECK CONSTRAINT [FK_Empleado_documento_Tipo_documento]
GO
ALTER TABLE [dbo].[Empleado_documento]  WITH CHECK ADD  CONSTRAINT [FK_EmpleadoDocumento_Empleado] FOREIGN KEY([ID_Empleado])
REFERENCES [dbo].[Empleado] ([ID_Empleado])
GO
ALTER TABLE [dbo].[Empleado_documento] CHECK CONSTRAINT [FK_EmpleadoDocumento_Empleado]
GO
ALTER TABLE [dbo].[Factura_Detalle]  WITH CHECK ADD  CONSTRAINT [FK_Factura_Detalle_Facturas] FOREIGN KEY([ID_Parametro])
REFERENCES [dbo].[Facturas] ([ID_Parametro])
GO
ALTER TABLE [dbo].[Factura_Detalle] CHECK CONSTRAINT [FK_Factura_Detalle_Facturas]
GO
ALTER TABLE [dbo].[Factura_Detalle]  WITH CHECK ADD  CONSTRAINT [FK_Factura_Detalle_IN_RE] FOREIGN KEY([ID_IN_RE])
REFERENCES [dbo].[IN_RE] ([ID_IN_RE])
GO
ALTER TABLE [dbo].[Factura_Detalle] CHECK CONSTRAINT [FK_Factura_Detalle_IN_RE]
GO
ALTER TABLE [dbo].[Facturas]  WITH CHECK ADD  CONSTRAINT [FK_Facturas_pago_detalle] FOREIGN KEY([ID_pago])
REFERENCES [dbo].[pago_detalle] ([ID_pago])
GO
ALTER TABLE [dbo].[Facturas] CHECK CONSTRAINT [FK_Facturas_pago_detalle]
GO
ALTER TABLE [dbo].[Facturas]  WITH CHECK ADD  CONSTRAINT [FK_Facturas_UsuariosCliente] FOREIGN KEY([ID_Usuario_ClienteF])
REFERENCES [dbo].[Usuarios_cliente] ([ID_Usuario_ClienteF])
GO
ALTER TABLE [dbo].[Facturas] CHECK CONSTRAINT [FK_Facturas_UsuariosCliente]
GO
ALTER TABLE [dbo].[Gerentes]  WITH CHECK ADD  CONSTRAINT [FK_Gerente_Sucursal] FOREIGN KEY([ID_sucursal])
REFERENCES [dbo].[Sucursales] ([ID_sucursal])
GO
ALTER TABLE [dbo].[Gerentes] CHECK CONSTRAINT [FK_Gerente_Sucursal]
GO
ALTER TABLE [dbo].[historial_ordenes_repartidor]  WITH CHECK ADD  CONSTRAINT [FK_historial_ordenes_repartidor_repartidor] FOREIGN KEY([ID_Repartidor])
REFERENCES [dbo].[Empleado] ([ID_Empleado])
GO
ALTER TABLE [dbo].[historial_ordenes_repartidor] CHECK CONSTRAINT [FK_historial_ordenes_repartidor_repartidor]
GO
ALTER TABLE [dbo].[IM_FA]  WITH CHECK ADD  CONSTRAINT [FK_IM_FA_Facturas] FOREIGN KEY([ID_Parametro])
REFERENCES [dbo].[Facturas] ([ID_Parametro])
GO
ALTER TABLE [dbo].[IM_FA] CHECK CONSTRAINT [FK_IM_FA_Facturas]
GO
ALTER TABLE [dbo].[IM_FA]  WITH CHECK ADD  CONSTRAINT [FK_IM_FA_Impuestos] FOREIGN KEY([ID_Impuesto])
REFERENCES [dbo].[Impuestos] ([ID_Impuesto])
GO
ALTER TABLE [dbo].[IM_FA] CHECK CONSTRAINT [FK_IM_FA_Impuestos]
GO
ALTER TABLE [dbo].[Impuesto_Categoria]  WITH CHECK ADD  CONSTRAINT [FK_ImpCat_Categoria] FOREIGN KEY([ID_Categoria])
REFERENCES [dbo].[categorias] ([ID_Categoria])
GO
ALTER TABLE [dbo].[Impuesto_Categoria] CHECK CONSTRAINT [FK_ImpCat_Categoria]
GO
ALTER TABLE [dbo].[Impuesto_Categoria]  WITH CHECK ADD  CONSTRAINT [FK_ImpCat_Impuesto] FOREIGN KEY([ID_Impuesto])
REFERENCES [dbo].[Impuestos] ([ID_Impuesto])
GO
ALTER TABLE [dbo].[Impuesto_Categoria] CHECK CONSTRAINT [FK_ImpCat_Impuesto]
GO
ALTER TABLE [dbo].[Impuesto_tasa_historica]  WITH CHECK ADD  CONSTRAINT [FK_ImpTasaHist_Impuestos] FOREIGN KEY([ID_Impuesto])
REFERENCES [dbo].[Impuestos] ([ID_Impuesto])
GO
ALTER TABLE [dbo].[Impuesto_tasa_historica] CHECK CONSTRAINT [FK_ImpTasaHist_Impuestos]
GO
ALTER TABLE [dbo].[Impuestos]  WITH CHECK ADD  CONSTRAINT [FK_Impuestos_Categorias] FOREIGN KEY([ID_Categoria])
REFERENCES [dbo].[categorias] ([ID_Categoria])
GO
ALTER TABLE [dbo].[Impuestos] CHECK CONSTRAINT [FK_Impuestos_Categorias]
GO
ALTER TABLE [dbo].[IN_RE]  WITH CHECK ADD  CONSTRAINT [FK_IN_RE_Insumos] FOREIGN KEY([ID_Insumo])
REFERENCES [dbo].[Insumos] ([ID_Insumo])
GO
ALTER TABLE [dbo].[IN_RE] CHECK CONSTRAINT [FK_IN_RE_Insumos]
GO
ALTER TABLE [dbo].[IN_RE]  WITH CHECK ADD  CONSTRAINT [FK_IN_RE_Recetas] FOREIGN KEY([ID_Receta])
REFERENCES [dbo].[Recetas] ([ID_Receta])
ON DELETE CASCADE
GO
ALTER TABLE [dbo].[IN_RE] CHECK CONSTRAINT [FK_IN_RE_Recetas]
GO
ALTER TABLE [dbo].[IN_RE]  WITH CHECK ADD  CONSTRAINT [FK_IN_RE_Sucursales] FOREIGN KEY([ID_sucursal])
REFERENCES [dbo].[Sucursales] ([ID_sucursal])
GO
ALTER TABLE [dbo].[IN_RE] CHECK CONSTRAINT [FK_IN_RE_Sucursales]
GO
ALTER TABLE [dbo].[IN_RE]  WITH CHECK ADD  CONSTRAINT [FK_IN_RE_UnidadesMedida] FOREIGN KEY([ID_Unidad])
REFERENCES [dbo].[Unidades_medida] ([ID_Unidad])
ON UPDATE CASCADE
ON DELETE CASCADE
GO
ALTER TABLE [dbo].[IN_RE] CHECK CONSTRAINT [FK_IN_RE_UnidadesMedida]
GO
ALTER TABLE [dbo].[Insumo_Precio_historico]  WITH CHECK ADD  CONSTRAINT [FK_Insumo_Precio_historico_Insumos] FOREIGN KEY([ID_Insumo])
REFERENCES [dbo].[Insumos] ([ID_Insumo])
GO
ALTER TABLE [dbo].[Insumo_Precio_historico] CHECK CONSTRAINT [FK_Insumo_Precio_historico_Insumos]
GO
ALTER TABLE [dbo].[Insumos]  WITH NOCHECK ADD  CONSTRAINT [FK_Insumos_categorias] FOREIGN KEY([ID_Categoria])
REFERENCES [dbo].[categorias] ([ID_Categoria])
GO
ALTER TABLE [dbo].[Insumos] CHECK CONSTRAINT [FK_Insumos_categorias]
GO
ALTER TABLE [dbo].[Insumos]  WITH CHECK ADD  CONSTRAINT [FK_Insumos_Sucursales] FOREIGN KEY([ID_sucursal])
REFERENCES [dbo].[Sucursales] ([ID_sucursal])
GO
ALTER TABLE [dbo].[Insumos] CHECK CONSTRAINT [FK_Insumos_Sucursales]
GO
ALTER TABLE [dbo].[Insumos]  WITH NOCHECK ADD  CONSTRAINT [FK_Insumos_Unidades_medida] FOREIGN KEY([ID_Unidad])
REFERENCES [dbo].[Unidades_medida] ([ID_Unidad])
GO
ALTER TABLE [dbo].[Insumos] CHECK CONSTRAINT [FK_Insumos_Unidades_medida]
GO
ALTER TABLE [dbo].[Jefe_de_cocina]  WITH CHECK ADD  CONSTRAINT [FK_Jefe_Sucursal] FOREIGN KEY([ID_sucursal])
REFERENCES [dbo].[Sucursales] ([ID_sucursal])
GO
ALTER TABLE [dbo].[Jefe_de_cocina] CHECK CONSTRAINT [FK_Jefe_Sucursal]
GO
ALTER TABLE [dbo].[Metodo_de_pago]  WITH CHECK ADD  CONSTRAINT [FK_MetodoPago_UsuarioCliente] FOREIGN KEY([ID_Usuario_ClienteF])
REFERENCES [dbo].[Usuarios_cliente] ([ID_Usuario_ClienteF])
ON UPDATE CASCADE
ON DELETE CASCADE
GO
ALTER TABLE [dbo].[Metodo_de_pago] CHECK CONSTRAINT [FK_MetodoPago_UsuarioCliente]
GO
ALTER TABLE [dbo].[ORD_REC]  WITH CHECK ADD  CONSTRAINT [FK_ORD_REC_Factura] FOREIGN KEY([ID_Parametro])
REFERENCES [dbo].[Facturas] ([ID_Parametro])
GO
ALTER TABLE [dbo].[ORD_REC] CHECK CONSTRAINT [FK_ORD_REC_Factura]
GO
ALTER TABLE [dbo].[ORD_REC]  WITH CHECK ADD  CONSTRAINT [FK_ORD_REC_Orden_Cliente] FOREIGN KEY([ID_Orden_cliente])
REFERENCES [dbo].[Orden_Cliente] ([ID_Orden_cliente])
GO
ALTER TABLE [dbo].[ORD_REC] CHECK CONSTRAINT [FK_ORD_REC_Orden_Cliente]
GO
ALTER TABLE [dbo].[ORD_REC]  WITH CHECK ADD  CONSTRAINT [FK_ORD_REC_Recetas] FOREIGN KEY([ID_Receta])
REFERENCES [dbo].[Recetas] ([ID_Receta])
ON DELETE CASCADE
GO
ALTER TABLE [dbo].[ORD_REC] CHECK CONSTRAINT [FK_ORD_REC_Recetas]
GO
ALTER TABLE [dbo].[ORD_REC]  WITH CHECK ADD  CONSTRAINT [FK_ORD_REC_Repartidores] FOREIGN KEY([ID_Repartidor])
REFERENCES [dbo].[Repartidores] ([ID_Repartidor])
GO
ALTER TABLE [dbo].[ORD_REC] CHECK CONSTRAINT [FK_ORD_REC_Repartidores]
GO
ALTER TABLE [dbo].[Orden_Cliente]  WITH CHECK ADD  CONSTRAINT [FK_Orden_Cliente_Usuario_cliente] FOREIGN KEY([ID_Usuario_ClienteF])
REFERENCES [dbo].[Usuarios_cliente] ([ID_Usuario_ClienteF])
GO
ALTER TABLE [dbo].[Orden_Cliente] CHECK CONSTRAINT [FK_Orden_Cliente_Usuario_cliente]
GO
ALTER TABLE [dbo].[Orden_Compra_a_los_Proveedores]  WITH CHECK ADD  CONSTRAINT [FK_Orden_Compra_a_los_Proveedores_Facturas] FOREIGN KEY([ID_Parametro])
REFERENCES [dbo].[Facturas] ([ID_Parametro])
GO
ALTER TABLE [dbo].[Orden_Compra_a_los_Proveedores] CHECK CONSTRAINT [FK_Orden_Compra_a_los_Proveedores_Facturas]
GO
ALTER TABLE [dbo].[Orden_Compra_a_los_Proveedores]  WITH CHECK ADD  CONSTRAINT [FK_Orden_Compra_a_los_Proveedores_Insumos] FOREIGN KEY([ID_Insumo])
REFERENCES [dbo].[Insumos] ([ID_Insumo])
GO
ALTER TABLE [dbo].[Orden_Compra_a_los_Proveedores] CHECK CONSTRAINT [FK_Orden_Compra_a_los_Proveedores_Insumos]
GO
ALTER TABLE [dbo].[Orden_Compra_a_los_Proveedores]  WITH CHECK ADD  CONSTRAINT [FK_Orden_Compra_a_los_Proveedores_Proveedores] FOREIGN KEY([ID_Proveedor])
REFERENCES [dbo].[Proveedores] ([ID_Proveedor])
GO
ALTER TABLE [dbo].[Orden_Compra_a_los_Proveedores] CHECK CONSTRAINT [FK_Orden_Compra_a_los_Proveedores_Proveedores]
GO
ALTER TABLE [dbo].[Orden_Entrega]  WITH CHECK ADD  CONSTRAINT [FK_Orden_Entrega_Direccion_del_cliente] FOREIGN KEY([ID_US_CO])
REFERENCES [dbo].[Direccion_del_cliente] ([ID_US_CO])
GO
ALTER TABLE [dbo].[Orden_Entrega] CHECK CONSTRAINT [FK_Orden_Entrega_Direccion_del_cliente]
GO
ALTER TABLE [dbo].[Orden_Entrega]  WITH CHECK ADD  CONSTRAINT [FK_Orden_Entrega_Direcciones] FOREIGN KEY([ID_Direccion])
REFERENCES [dbo].[Direcciones] ([ID_Direccion])
GO
ALTER TABLE [dbo].[Orden_Entrega] CHECK CONSTRAINT [FK_Orden_Entrega_Direcciones]
GO
ALTER TABLE [dbo].[Orden_Entrega]  WITH CHECK ADD  CONSTRAINT [FK_Orden_Entrega_Empleado_Repartidor] FOREIGN KEY([ID_Empleado_Repartidor])
REFERENCES [dbo].[Empleado] ([ID_Empleado])
GO
ALTER TABLE [dbo].[Orden_Entrega] CHECK CONSTRAINT [FK_Orden_Entrega_Empleado_Repartidor]
GO
ALTER TABLE [dbo].[Orden_Entrega]  WITH CHECK ADD  CONSTRAINT [FK_Orden_Entrega_Facturas] FOREIGN KEY([ID_Parametro])
REFERENCES [dbo].[Facturas] ([ID_Parametro])
GO
ALTER TABLE [dbo].[Orden_Entrega] CHECK CONSTRAINT [FK_Orden_Entrega_Facturas]
GO
ALTER TABLE [dbo].[Orden_Entrega]  WITH CHECK ADD  CONSTRAINT [FK_Orden_Entrega_Sucursales] FOREIGN KEY([ID_sucursal])
REFERENCES [dbo].[Sucursales] ([ID_sucursal])
GO
ALTER TABLE [dbo].[Orden_Entrega] CHECK CONSTRAINT [FK_Orden_Entrega_Sucursales]
GO
ALTER TABLE [dbo].[Orden_Entrega]  WITH CHECK ADD  CONSTRAINT [FK_Orden_Entrega_Usuarios_cliente] FOREIGN KEY([ID_Usuario_ClienteF])
REFERENCES [dbo].[Usuarios_cliente] ([ID_Usuario_ClienteF])
GO
ALTER TABLE [dbo].[Orden_Entrega] CHECK CONSTRAINT [FK_Orden_Entrega_Usuarios_cliente]
GO
ALTER TABLE [dbo].[Ordenes_Proveedores]  WITH CHECK ADD  CONSTRAINT [FK_Ordenes_Proveedores_Sucursales] FOREIGN KEY([ID_Sucursal])
REFERENCES [dbo].[Sucursales] ([ID_sucursal])
GO
ALTER TABLE [dbo].[Ordenes_Proveedores] CHECK CONSTRAINT [FK_Ordenes_Proveedores_Sucursales]
GO
ALTER TABLE [dbo].[Ordenes_Proveedores]  WITH CHECK ADD  CONSTRAINT [FK_Ordenes_Proveedores_Unidades_medida] FOREIGN KEY([ID_Unidad])
REFERENCES [dbo].[Unidades_medida] ([ID_Unidad])
GO
ALTER TABLE [dbo].[Ordenes_Proveedores] CHECK CONSTRAINT [FK_Ordenes_Proveedores_Unidades_medida]
GO
ALTER TABLE [dbo].[Ordenes_Proveedores]  WITH CHECK ADD  CONSTRAINT [FK_OrdenesProv_Empleado] FOREIGN KEY([ID_Empleado_Encargado])
REFERENCES [dbo].[Empleado] ([ID_Empleado])
GO
ALTER TABLE [dbo].[Ordenes_Proveedores] CHECK CONSTRAINT [FK_OrdenesProv_Empleado]
GO
ALTER TABLE [dbo].[Ordenes_Proveedores]  WITH CHECK ADD  CONSTRAINT [FK_OrdenesProv_Proveedor] FOREIGN KEY([ID_Proveedor])
REFERENCES [dbo].[Proveedores] ([ID_Proveedor])
GO
ALTER TABLE [dbo].[Ordenes_Proveedores] CHECK CONSTRAINT [FK_OrdenesProv_Proveedor]
GO
ALTER TABLE [dbo].[Ordenes_Proveedores]  WITH CHECK ADD  CONSTRAINT [FK_OrdenesProv_Sucursal] FOREIGN KEY([ID_Sucursal])
REFERENCES [dbo].[Sucursales] ([ID_sucursal])
GO
ALTER TABLE [dbo].[Ordenes_Proveedores] CHECK CONSTRAINT [FK_OrdenesProv_Sucursal]
GO
ALTER TABLE [dbo].[Ordenes_Proveedores_Detalle]  WITH CHECK ADD  CONSTRAINT [FK_OPD_UnidadRecibida] FOREIGN KEY([ID_Unidad_Recibida])
REFERENCES [dbo].[Unidades_medida] ([ID_Unidad])
GO
ALTER TABLE [dbo].[Ordenes_Proveedores_Detalle] CHECK CONSTRAINT [FK_OPD_UnidadRecibida]
GO
ALTER TABLE [dbo].[Ordenes_Proveedores_Detalle]  WITH CHECK ADD  CONSTRAINT [FK_Ordenes_Prov_Detalle_Insumos] FOREIGN KEY([ID_Insumo])
REFERENCES [dbo].[Insumos] ([ID_Insumo])
GO
ALTER TABLE [dbo].[Ordenes_Proveedores_Detalle] CHECK CONSTRAINT [FK_Ordenes_Prov_Detalle_Insumos]
GO
ALTER TABLE [dbo].[Ordenes_Proveedores_Detalle]  WITH CHECK ADD  CONSTRAINT [FK_Ordenes_Prov_Detalle_Orden] FOREIGN KEY([ID_Orden_Proveedor])
REFERENCES [dbo].[Ordenes_Proveedores] ([ID_Orden_Proveedor])
GO
ALTER TABLE [dbo].[Ordenes_Proveedores_Detalle] CHECK CONSTRAINT [FK_Ordenes_Prov_Detalle_Orden]
GO
ALTER TABLE [dbo].[Ordenes_Proveedores_Detalle]  WITH CHECK ADD  CONSTRAINT [FK_Ordenes_Prov_Detalle_Unidades] FOREIGN KEY([ID_Unidad])
REFERENCES [dbo].[Unidades_medida] ([ID_Unidad])
GO
ALTER TABLE [dbo].[Ordenes_Proveedores_Detalle] CHECK CONSTRAINT [FK_Ordenes_Prov_Detalle_Unidades]
GO
ALTER TABLE [dbo].[pago_detalle]  WITH CHECK ADD  CONSTRAINT [FK_pago_detalle_Metodos_money] FOREIGN KEY([ID_Metodo])
REFERENCES [dbo].[Metodos_money] ([ID_Metodo])
GO
ALTER TABLE [dbo].[pago_detalle] CHECK CONSTRAINT [FK_pago_detalle_Metodos_money]
GO
ALTER TABLE [dbo].[Pagos_cliente]  WITH CHECK ADD  CONSTRAINT [FK_PagosCliente_MetodosMoney] FOREIGN KEY([ID_Metodo])
REFERENCES [dbo].[Metodos_money] ([ID_Metodo])
GO
ALTER TABLE [dbo].[Pagos_cliente] CHECK CONSTRAINT [FK_PagosCliente_MetodosMoney]
GO
ALTER TABLE [dbo].[Pagos_cliente]  WITH CHECK ADD  CONSTRAINT [FK_PagosCliente_UsuarioCliente] FOREIGN KEY([ID_Usuario_ClienteF])
REFERENCES [dbo].[Usuarios_cliente] ([ID_Usuario_ClienteF])
GO
ALTER TABLE [dbo].[Pagos_cliente] CHECK CONSTRAINT [FK_PagosCliente_UsuarioCliente]
GO
ALTER TABLE [dbo].[Proveedor_documento]  WITH CHECK ADD  CONSTRAINT [FK_Proveedor_documento_Proveedores] FOREIGN KEY([ID_Proveedor])
REFERENCES [dbo].[Proveedores] ([ID_Proveedor])
GO
ALTER TABLE [dbo].[Proveedor_documento] CHECK CONSTRAINT [FK_Proveedor_documento_Proveedores]
GO
ALTER TABLE [dbo].[Proveedor_documento]  WITH CHECK ADD  CONSTRAINT [FK_Proveedor_documento_Tipo_documentos] FOREIGN KEY([tipo_doc])
REFERENCES [dbo].[Tipo_documentos] ([tipo_doc])
GO
ALTER TABLE [dbo].[Proveedor_documento] CHECK CONSTRAINT [FK_Proveedor_documento_Tipo_documentos]
GO
ALTER TABLE [dbo].[Proveedor_Insumo]  WITH CHECK ADD  CONSTRAINT [FK_Proveedor_Insumo_Insumo] FOREIGN KEY([ID_Insumo])
REFERENCES [dbo].[Insumos] ([ID_Insumo])
GO
ALTER TABLE [dbo].[Proveedor_Insumo] CHECK CONSTRAINT [FK_Proveedor_Insumo_Insumo]
GO
ALTER TABLE [dbo].[Proveedor_Insumo]  WITH CHECK ADD  CONSTRAINT [FK_Proveedor_Insumo_Proveedor] FOREIGN KEY([ID_Proveedor])
REFERENCES [dbo].[Proveedores] ([ID_Proveedor])
GO
ALTER TABLE [dbo].[Proveedor_Insumo] CHECK CONSTRAINT [FK_Proveedor_Insumo_Proveedor]
GO
ALTER TABLE [dbo].[Recetas]  WITH CHECK ADD  CONSTRAINT [FK_Receta_Jefe_de_cocina] FOREIGN KEY([ID_Jefe_de_cocina])
REFERENCES [dbo].[Jefe_de_cocina] ([ID_Jefe_de_cocina])
GO
ALTER TABLE [dbo].[Recetas] CHECK CONSTRAINT [FK_Receta_Jefe_de_cocina]
GO
ALTER TABLE [dbo].[Recetas]  WITH CHECK ADD  CONSTRAINT [FK_Recetas_Sucursales] FOREIGN KEY([ID_sucursal])
REFERENCES [dbo].[Sucursales] ([ID_sucursal])
GO
ALTER TABLE [dbo].[Recetas] CHECK CONSTRAINT [FK_Recetas_Sucursales]
GO
ALTER TABLE [dbo].[recetas_precio_historico]  WITH CHECK ADD  CONSTRAINT [FK_receta_precio_hist_Recetas] FOREIGN KEY([ID_Receta])
REFERENCES [dbo].[Recetas] ([ID_Receta])
GO
ALTER TABLE [dbo].[recetas_precio_historico] CHECK CONSTRAINT [FK_receta_precio_hist_Recetas]
GO
ALTER TABLE [dbo].[Sucursales]  WITH CHECK ADD  CONSTRAINT [FK_Sucursales_Direcciones] FOREIGN KEY([ID_Direccion])
REFERENCES [dbo].[Direcciones] ([ID_Direccion])
GO
ALTER TABLE [dbo].[Sucursales] CHECK CONSTRAINT [FK_Sucursales_Direcciones]
GO
ALTER TABLE [dbo].[Usuarios_cliente]  WITH CHECK ADD  CONSTRAINT [FK_Usuario_cliente_Sucursal] FOREIGN KEY([ID_sucursal])
REFERENCES [dbo].[Sucursales] ([ID_sucursal])
GO
ALTER TABLE [dbo].[Usuarios_cliente] CHECK CONSTRAINT [FK_Usuario_cliente_Sucursal]
GO
ALTER TABLE [dbo].[categorias]  WITH CHECK ADD  CONSTRAINT [CK_categorias_tipo] CHECK  (([tipo]=(3) OR [tipo]=(2) OR [tipo]=(1)))
GO
ALTER TABLE [dbo].[categorias] CHECK CONSTRAINT [CK_categorias_tipo]
GO
ALTER TABLE [dbo].[django_admin_log]  WITH CHECK ADD  CONSTRAINT [django_admin_log_action_flag_a8637d59_check] CHECK  (([action_flag]>=(0)))
GO
ALTER TABLE [dbo].[django_admin_log] CHECK CONSTRAINT [django_admin_log_action_flag_a8637d59_check]
GO
ALTER TABLE [dbo].[historial_ordenes_repartidor]  WITH CHECK ADD  CONSTRAINT [CK_historial_ordenes_repartidor_estado] CHECK  (([Estado_Final]=(4) OR [Estado_Final]=(3)))
GO
ALTER TABLE [dbo].[historial_ordenes_repartidor] CHECK CONSTRAINT [CK_historial_ordenes_repartidor_estado]
GO
ALTER TABLE [dbo].[IN_RE]  WITH CHECK ADD  CONSTRAINT [CHK_CantidadUsada_Pos] CHECK  (([cantidad_usada]>=(0)))
GO
ALTER TABLE [dbo].[IN_RE] CHECK CONSTRAINT [CHK_CantidadUsada_Pos]
GO
ALTER TABLE [dbo].[Metodos_money]  WITH CHECK ADD  CONSTRAINT [CK_Metodos_money_Tipo] CHECK  (([Tipo]=(3) OR [Tipo]=(2) OR [Tipo]=(1)))
GO
ALTER TABLE [dbo].[Metodos_money] CHECK CONSTRAINT [CK_Metodos_money_Tipo]
GO
ALTER TABLE [dbo].[Ordenes_Proveedores]  WITH CHECK ADD  CONSTRAINT [CK_OrdenesProv_Estado] CHECK  (([Estado]>=(0) AND [Estado]<=(4)))
GO
ALTER TABLE [dbo].[Ordenes_Proveedores] CHECK CONSTRAINT [CK_OrdenesProv_Estado]
GO
ALTER TABLE [dbo].[Pagos_cliente]  WITH CHECK ADD  CONSTRAINT [CK_PagosCliente_NumeroTarjeta] CHECK  (([Numero_tarjeta] IS NULL OR [Numero_tarjeta] like '[0-9][0-9][0-9][0-9]'))
GO
ALTER TABLE [dbo].[Pagos_cliente] CHECK CONSTRAINT [CK_PagosCliente_NumeroTarjeta]
GO
ALTER TABLE [dbo].[Tipo_documentos]  WITH CHECK ADD  CONSTRAINT [CK_Tipo_documentos_tipo] CHECK  (([tipo]=(4) OR [tipo]=(3) OR [tipo]=(2) OR [tipo]=(1)))
GO
ALTER TABLE [dbo].[Tipo_documentos] CHECK CONSTRAINT [CK_Tipo_documentos_tipo]
GO
/****** Object:  Trigger [dbo].[TR_CAI_Secuencia_Historico]    Script Date: 2/2/2026 09:13:33 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE TRIGGER [dbo].[TR_CAI_Secuencia_Historico]
ON [dbo].[CAI]
AFTER INSERT, UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    /*
        inserted  = valores nuevos
        deleted   = valores anteriores (solo en UPDATE)

        Queremos guardar histórico SOLO cuando:
        - La secuencia cambie (UPDATE), o
        - (Opcional) se cree un CAI nuevo → si NO quieres esto, quita la condición d.ID_Cai IS NULL
    */

    INSERT INTO dbo.CAI_Historico
    (
        ID_Cai,
        Fecha_Registro,
        Fecha_Emision,
        Fecha_Final,
        Rango_Inicial,
        Rango_Final,
        Secuencia,
        estado,
        ID_sucursal
    )
    SELECT
        i.ID_Cai,
        SYSUTCDATETIME(),          -- Fecha/hora de registro del histórico
        i.Fecha_Emision,
        i.Fecha_Final,
        i.Rango_Inicial,
        i.Rango_Final,
        i.Secuencia,
        i.estado,
        i.ID_sucursal
    FROM inserted i
    LEFT JOIN deleted d
        ON d.ID_Cai = i.ID_Cai
    WHERE
        -- Nuevo CAI (no había registro antes)
        d.ID_Cai IS NULL
        -- O cambió la secuencia
        OR ISNULL(i.Secuencia, -1) <> ISNULL(d.Secuencia, -1);
END;
GO
ALTER TABLE [dbo].[CAI] ENABLE TRIGGER [TR_CAI_Secuencia_Historico]
GO
/****** Object:  Trigger [dbo].[TR_Impuestos_Tasa_Historica]    Script Date: 2/2/2026 09:13:33 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TRIGGER [dbo].[TR_Impuestos_Tasa_Historica]
ON [dbo].[Impuestos]
AFTER INSERT, UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    UPDATE h
    SET fecha_fin = GETDATE()
    FROM dbo.Impuesto_tasa_historica h
    JOIN inserted i ON i.ID_Impuesto = h.ID_Impuesto
    WHERE h.fecha_fin IS NULL
      AND h.tasa <> i.tasa;

    INSERT INTO dbo.Impuesto_tasa_historica (ID_Impuesto, fecha_inicio, tasa)
    SELECT i.ID_Impuesto, GETDATE(), i.tasa
    FROM inserted i
    LEFT JOIN dbo.Impuesto_tasa_historica h
      ON h.ID_Impuesto = i.ID_Impuesto
     AND h.fecha_fin IS NULL
    WHERE h.ID_Impuesto IS NULL
       OR h.tasa <> i.tasa;
END;
GO
ALTER TABLE [dbo].[Impuestos] ENABLE TRIGGER [TR_Impuestos_Tasa_Historica]
GO
/****** Object:  Trigger [dbo].[TR_CalcularPrecioInRe]    Script Date: 2/2/2026 09:13:33 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TRIGGER [dbo].[TR_CalcularPrecioInRe]
ON [dbo].[IN_RE]
AFTER INSERT
AS
BEGIN
    SET NOCOUNT ON;

    IF TRIGGER_NESTLEVEL() > 1 RETURN;

    UPDATE ir
    SET ir.precio_final = 
        CASE 
            WHEN i.peso_individual = 0 OR i.peso_individual IS NULL THEN 0
            ELSE 
                (i.precio_lempiras / i.peso_individual)
                * ir.cantidad_usada
                * (uc_insumo.Equivalente / uc_receta.Equivalente)
        END
    FROM IN_RE ir
    INNER JOIN inserted ins ON ir.ID_IN_RE = ins.ID_IN_RE
    INNER JOIN Insumos i ON i.ID_Insumo = ir.ID_Insumo
    INNER JOIN Unidades_Conversion uc_insumo ON uc_insumo.ID_Unidad = i.ID_Unidad
    INNER JOIN Unidades_Conversion uc_receta ON uc_receta.ID_Unidad = ir.ID_Unidad;
END;
GO
ALTER TABLE [dbo].[IN_RE] ENABLE TRIGGER [TR_CalcularPrecioInRe]
GO
/****** Object:  Trigger [dbo].[TR_HistorialPrecioReceta]    Script Date: 2/2/2026 09:13:33 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE TRIGGER [dbo].[TR_HistorialPrecioReceta]
ON [dbo].[IN_RE]
AFTER INSERT, UPDATE, DELETE
AS
BEGIN
    SET NOCOUNT ON;

    DECLARE @Hoy DATE = CONVERT(date, GETDATE());

    ;WITH RecetasAfectadas AS (
        SELECT DISTINCT ID_Receta
        FROM inserted
        WHERE ID_Receta IS NOT NULL

        UNION

        SELECT DISTINCT ID_Receta
        FROM deleted
        WHERE ID_Receta IS NOT NULL
    ),
    Totales AS (
        SELECT
            r.ID_Receta,
            TotalCosto = ISNULL((
                SELECT SUM(CAST(ir.precio_final AS DECIMAL(10,2)))
                FROM dbo.IN_RE AS ir
                WHERE ir.ID_Receta = r.ID_Receta
                  AND ir.Activo = 1
            ), 0)
        FROM RecetasAfectadas AS r
    )
    SELECT 
        t.ID_Receta,
        t.TotalCosto,
        h.ID_Receta_precio_historico,
        h.Costo       AS CostoAnterior,
        h.Fecha_Fin   AS FechaFinAnterior
    INTO #TmpDatos
    FROM Totales t
    OUTER APPLY (
        SELECT TOP (1)
            h.ID_Receta_precio_historico,
            h.Costo,
            h.Fecha_Fin
        FROM dbo.recetas_precio_historico h
        WHERE h.ID_Receta = t.ID_Receta
        ORDER BY h.Fecha_inicio DESC,
                 h.ID_Receta_precio_historico DESC
    ) h;

    -- 1) Cerrar registro anterior si el costo cambió
    UPDATE h
    SET h.Fecha_Fin = @Hoy
    FROM dbo.recetas_precio_historico h
    JOIN #TmpDatos d
      ON d.ID_Receta_precio_historico = h.ID_Receta_precio_historico
    WHERE d.CostoAnterior IS NOT NULL
      AND d.TotalCosto <> d.CostoAnterior
      AND h.Fecha_Fin IS NULL;

    -- 2) Insertar nuevo registro si:
    --    - No había historial
    --    - O el costo es distinto al anterior
    INSERT INTO dbo.recetas_precio_historico (ID_Receta, Costo, Fecha_inicio, Fecha_Fin)
    SELECT
        d.ID_Receta,
        d.TotalCosto,
        @Hoy,
        NULL
    FROM #TmpDatos d
    WHERE (d.CostoAnterior IS NULL AND d.TotalCosto IS NOT NULL)
       OR (d.CostoAnterior IS NOT NULL AND d.TotalCosto <> d.CostoAnterior);

    DROP TABLE #TmpDatos;
END;
GO
ALTER TABLE [dbo].[IN_RE] ENABLE TRIGGER [TR_HistorialPrecioReceta]
GO
/****** Object:  Trigger [dbo].[TR_IN_RE_SyncSucursal]    Script Date: 2/2/2026 09:13:33 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE TRIGGER [dbo].[TR_IN_RE_SyncSucursal]
ON [dbo].[IN_RE]
AFTER INSERT, UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    UPDATE ir
    SET ir.ID_sucursal = r.ID_sucursal
    FROM dbo.IN_RE ir
    INNER JOIN inserted i ON i.ID_IN_RE = ir.ID_IN_RE
    INNER JOIN dbo.Recetas r ON r.ID_Receta = ir.ID_Receta;
END
GO
ALTER TABLE [dbo].[IN_RE] ENABLE TRIGGER [TR_IN_RE_SyncSucursal]
GO
/****** Object:  Trigger [dbo].[TR_RecalcularInRePorInsumo]    Script Date: 2/2/2026 09:13:34 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TRIGGER [dbo].[TR_RecalcularInRePorInsumo]
ON [dbo].[Insumos]
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    IF NOT UPDATE(precio_lempiras) AND NOT UPDATE(peso_individual)
        RETURN;

    ;WITH Cambios AS (
        SELECT 
            i.ID_Insumo,
            i.precio_lempiras,
            i.peso_individual,
            u.Equivalente AS EqInsumo
        FROM inserted i
        INNER JOIN Unidades_Conversion u ON u.ID_Unidad = i.ID_Unidad
    )
    UPDATE ir
    SET ir.precio_final =
        CASE
            WHEN c.peso_individual IS NULL OR c.peso_individual = 0 THEN 0
            ELSE 
                (c.precio_lempiras / c.peso_individual)
                * ir.cantidad_usada
                * (c.EqInsumo / uc_receta.Equivalente)
        END
    FROM IN_RE ir
    INNER JOIN Cambios c ON ir.ID_Insumo = c.ID_Insumo
    INNER JOIN Unidades_Conversion uc_receta ON uc_receta.ID_Unidad = ir.ID_Unidad
    WHERE ir.Activo = 1;
END;
GO
ALTER TABLE [dbo].[Insumos] ENABLE TRIGGER [TR_RecalcularInRePorInsumo]
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'1 solicitado 2 pendiente 3 aceptado  4 rechazado' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'Orden_Compra_a_los_Proveedores', @level2type=N'COLUMN',@level2name=N'estado'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'1=efectivo 2=tarjeta 3=transferencia 4=mixto' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'Tipo_De_Pago', @level2type=N'COLUMN',@level2name=N'tipo'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'aqui me refiero a  1=peso 2=volumen 3=unidad 4=longitud' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'Unidades_medida', @level2type=N'COLUMN',@level2name=N'Tipo'
GO
USE [master]
GO
ALTER DATABASE [ALITAS EL COMELON SF] SET  READ_WRITE 
GO
